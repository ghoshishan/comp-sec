from server.server import Server

from phe import paillier, EncryptedNumber, PaillierPublicKey

server = Server()

pub_key, priv_key = paillier.generate_paillier_keypair()
X = [22, 53, 61, 62, 74]
V = [11, 40, 45]
X_transformed = [22, 53, 61, 62, 74, 11, 40, 45, 1, 1, 16334, 3746]
encrypted_X = [pub_key.encrypt(i) for i in X_transformed]
server.store_template(encrypted_X, pub_key.n)

Y = [21, 52, 61, 62, 74]
V = [11, 40, 45]
Y_transformed = [-42, -104, -122, -124, -
                 148, -22, -80, -90, 16186, 3746, 1, 1]
eucledian_distance = server.compute_euclidean(Y_transformed, server.tid)
eucledian_distance = priv_key.decrypt(
    EncryptedNumber(pub_key, eucledian_distance))
print(eucledian_distance)
res = server.make_decision(eucledian_distance)
if res == True:
    print("Authenticated")
else:
    print("Not Authenticated")
