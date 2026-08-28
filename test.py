import rlp from eth_hash.auto
import keccak


# ------------------------------------------------------------
# Utility: convert bytes → nibbles
# ------------------------------------------------------------
def bytes_to_nibbles(b):
    nibbles = []
    for byte in b:
        nibbles.append(byte >> 4)
        nibbles.append(byte & 0x0F)
    return nibbles


# ------------------------------------------------------------
# Hex-prefix (HP) encoding for leaf/extension nodes
# ------------------------------------------------------------
def hp_encode(nibbles, is_leaf):
    flag = 2 if is_leaf else 0

    if len(nibbles) % 2 == 1:
        # odd length: prefix = flag + 1
        prefix = [flag + 1, nibbles[0]]
        return bytes(prefix + nibbles[1:])
    else:
        # even length: prefix = flag
        prefix = [flag]
        return bytes(prefix + nibbles)


# ------------------------------------------------------------
# Node types
# ------------------------------------------------------------
class LeafNode:
    def __init__(self, key, value):
        self.key = key  # nibble list
        self.value = value

    def encode(self):
        return rlp.encode([hp_encode(self.key, is_leaf=True), self.value])


class ExtensionNode:
    def __init__(self, key, child):
        self.key = key  # nibble list
        self.child = child  # hash or inline node

    def encode(self):
        return rlp.encode([hp_encode(self.key, is_leaf=False), self.child])


class BranchNode:
    def __init__(self):
        self.children = [b""] * 16
        self.value = b""

    def encode(self):
        return rlp.encode(self.children + [self.value])


# ------------------------------------------------------------
# Trie class
# ------------------------------------------------------------
class MerklePatriciaTrie:
    def __init__(self):
        self.db = {}  # hash → encoded node
        self.root = b""

    def _store(self, encoded):
        if len(encoded) < 32:
            return encoded  # inline
        h = keccak(encoded)
        self.db[h] = encoded
        return h

    def insert(self, key, value):
        nibbles = bytes_to_nibbles(key.encode())
        self.root = self._insert_at(self.root, nibbles, value)

    def _insert_at(self, node_ref, key, value):
        if node_ref == b"":
            leaf = LeafNode(key, value)
            return self._store(leaf.encode())

        # decode existing node
        encoded = self.db.get(node_ref, node_ref)
        decoded = rlp.decode(encoded)

        # LEAF NODE
        if len(decoded) == 2 and decoded[0][0] in (0x20, 0x30):
            return self._insert_into_leaf(node_ref, decoded, key, value)

        # BRANCH NODE
        if len(decoded) == 17:
            return self._insert_into_branch(node_ref, decoded, key, value)

        # EXTENSION NODE
        return self._insert_into_extension(node_ref, decoded, key, value)

    # ------------------------------------------------------------
    # Insert into leaf
    # ------------------------------------------------------------
    def _insert_into_leaf(self, node_ref, decoded, key, value):
        # decode leaf key
        leaf_key = list(decoded[0])[1:]  # remove HP prefix
        common = 0
        while (
            common < len(leaf_key)
            and common < len(key)
            and leaf_key[common] == key[common]
        ):
            common += 1

        if common == len(leaf_key) and common == len(key):
            # exact match → replace value
            leaf = LeafNode(key, value)
            return self._store(leaf.encode())

        # create branch
        branch = BranchNode()

        # old leaf child
        if common < len(leaf_key):
            old_leaf = LeafNode(leaf_key[common + 1 :], decoded[1])
            branch.children[leaf_key[common]] = self._store(old_leaf.encode())
        else:
            branch.value = decoded[1]

        # new leaf child
        if common < len(key):
            new_leaf = LeafNode(key[common + 1 :], value)
            branch.children[key[common]] = self._store(new_leaf.encode())
        else:
            branch.value = value

        # if common prefix exists → extension node
        if common > 0:
            ext = ExtensionNode(key[:common], self._store(branch.encode()))
            return self._store(ext.encode())

        return self._store(branch.encode())

    # ------------------------------------------------------------
    # Insert into branch
    # ------------------------------------------------------------
    def _insert_into_branch(self, node_ref, decoded, key, value):
        branch = BranchNode()
        branch.children = decoded[:16]
        branch.value = decoded[16]

        if len(key) == 0:
            branch.value = value
            return self._store(branch.encode())

        idx = key[0]
        branch.children[idx] = self._insert_at(branch.children[idx], key[1:], value)
        return self._store(branch.encode())

    # ------------------------------------------------------------
    # Insert into extension
    # ------------------------------------------------------------
    def _insert_into_extension(self, node_ref, decoded, key, value):
        ext_key = list(decoded[0])[1:]  # remove HP prefix
        child_ref = decoded[1]

        common = 0
        while (
            common < len(ext_key)
            and common < len(key)
            and ext_key[common] == key[common]
        ):
            common += 1

        if common == len(ext_key):
            # continue into child
            new_child = self._insert_at(child_ref, key[common:], value)
            ext = ExtensionNode(ext_key, new_child)
            return self._store(ext.encode())

        # split extension
        branch = BranchNode()

        # old child
        old_ext = ExtensionNode(ext_key[common + 1 :], child_ref)
        branch.children[ext_key[common]] = self._store(old_ext.encode())

        # new leaf
        new_leaf = LeafNode(key[common + 1 :], value)
        branch.children[key[common]] = self._store(new_leaf.encode())

        if common > 0:
            ext = ExtensionNode(ext_key[:common], self._store(branch.encode()))
            return self._store(ext.encode())

        return self._store(branch.encode())


# ------------------------------------------------------------
# Example usage
# ------------------------------------------------------------
trie = MerklePatriciaTrie()
words = ["cat", "car", "dog"]

for w in words:
    trie.insert(w, w.encode())

print("Trie root hash:", trie.root.hex())
