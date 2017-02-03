class Des:
    """

    a simple DES encryption class for only EBC mode

    usage:

    obj = Des(key)
    encrypted_text = obj.encrypt(plain_text)
    plain_text = obj.decrypt(encrypted_text)

    key -> Bytes containing the encryption key, must be exactly 8 bytes

    """

    # Permutation and translation tables for DES
    __pc1 = [
        56, 48, 40, 32, 24, 16, 8,
        0, 57, 49, 41, 33, 25, 17,
        9, 1, 58, 50, 42, 34, 26,
        18, 10, 2, 59, 51, 43, 35,
        62, 54, 46, 38, 30, 22, 14,
        6, 61, 53, 45, 37, 29, 21,
        13, 5, 60, 52, 44, 36, 28,
        20, 12, 4, 27, 19, 11, 3
    ]

    # number left rotations of pc1
    __left_rotations = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

    # permuted choice key (table 2)
    __pc2 = [
        13, 16, 10, 23, 0, 4,
        2, 27, 14, 5, 20, 9,
        22, 18, 11, 3, 25, 7,
        15, 6, 26, 19, 12, 1,
        40, 51, 30, 36, 46, 54,
        29, 39, 50, 44, 32, 47,
        43, 48, 38, 55, 33, 52,
        45, 41, 49, 35, 28, 31
    ]

    # initial permutation IP
    __ip = [
        57, 49, 41, 33, 25, 17, 9, 1,
        59, 51, 43, 35, 27, 19, 11, 3,
        61, 53, 45, 37, 29, 21, 13, 5,
        63, 55, 47, 39, 31, 23, 15, 7,
        56, 48, 40, 32, 24, 16, 8, 0,
        58, 50, 42, 34, 26, 18, 10, 2,
        60, 52, 44, 36, 28, 20, 12, 4,
        62, 54, 46, 38, 30, 22, 14, 6
    ]

    # Expansion table for turning 32 bit blocks into 48 bits
    __expansion_table = [
        31, 0, 1, 2, 3, 4,
        3, 4, 5, 6, 7, 8,
        7, 8, 9, 10, 11, 12,
        11, 12, 13, 14, 15, 16,
        15, 16, 17, 18, 19, 20,
        19, 20, 21, 22, 23, 24,
        23, 24, 25, 26, 27, 28,
        27, 28, 29, 30, 31, 0
    ]

    # The (in)famous S-boxes
    __sbox = [
        # S1
        [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7,
         0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8,
         4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0,
         15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],

        # S2
        [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10,
         3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5,
         0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15,
         13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],

        # S3
        [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8,
         13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1,
         13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7,
         1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],

        # S4
        [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15,
         13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9,
         10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4,
         3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],

        # S5
        [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9,
         14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6,
         4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14,
         11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],

        # S6
        [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11,
         10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8,
         9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6,
         4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],

        # S7
        [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1,
         13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6,
         1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2,
         6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],

        # S8
        [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7,
         1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2,
         7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8,
         2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
    ]

    # 32-bit permutation function P used on the output of the S-boxes
    __p = [
        15, 6, 19, 20, 28, 11,
        27, 16, 0, 14, 22, 25,
        4, 17, 30, 9, 1, 7,
        23, 13, 31, 26, 2, 8,
        18, 12, 29, 5, 21, 10,
        3, 24
    ]

    # final permutation IP^-1
    __fp = [
        39, 7, 47, 15, 55, 23, 63, 31,
        38, 6, 46, 14, 54, 22, 62, 30,
        37, 5, 45, 13, 53, 21, 61, 29,
        36, 4, 44, 12, 52, 20, 60, 28,
        35, 3, 43, 11, 51, 19, 59, 27,
        34, 2, 42, 10, 50, 18, 58, 26,
        33, 1, 41, 9, 49, 17, 57, 25,
        32, 0, 40, 8, 48, 16, 56, 24
    ]

    ENCRYPT = 0
    DECRYPT = 1

    def __init__(self, key):
        if len(key) != 8:
            raise ValueError("Invalid DES key size. Key must be exactly 8 bytes long.")
        self.key_size = 8

        self.L = []
        self.R = []
        self.Kn = [[0] * 48] * 16  # 16 48-bit keys (K1 - K16)
        self.final = []
        self.block_size = 8
        self._set_key(key)

    def _set_key(self, key):
        """select 48-bit sub-key from the 64-bit key, store them in subkey set Kn"""

        # select 56 bits from the 64-bit key
        key = self._permutate(self.__pc1, self._string_to_bitlist(key))
        self.L = key[:28]
        self.R = key[28:]
        for i in range(0, 16):
            for j in range(0, self.__left_rotations[i]):
                self.L.append(self.L[0])
                del self.L[0]
                self.R.append(self.R[0])
                del self.R[0]
            # select 48 bits from 56 bits
            self.Kn[i] = self._permutate(self.__pc2, self.L + self.R)

    def _pad_data(self, data):
        """
        pad mode: PAD_PKCS5
        :param data: input data to pad
        :return padded data
        """
        pad_len = self.block_size - (len(data) % self.block_size)
        data += bytes([pad_len] * pad_len)
        return data

    def _unpad_data(self, data):
        """
        pad mode: PAD_PKCS5
        :param data: input data to unpad
        :return: unpadded data
        """
        pad_len = data[-1]
        data = data[:-pad_len]
        return data

    def _string_to_bitlist(self, data):
        """turn string data into list of bits"""
        l = len(data) * 8
        result = [0] * l
        pos = 0
        for ch in data:
            i = 7
            while i >= 0:
                # bit-wise operation
                if ch & (1 << i) != 0:
                    result[pos] = 1
                else:
                    result[pos] = 0
                pos += 1
                i -= 1
        return result

    def _bitlist_to_string(self, data):
        """turn list of bits into string"""
        result = []
        pos = 0
        c = 0
        while pos < len(data):
            c += data[pos] << (7 - (pos % 8))
            if pos % 8 == 7:
                result.append(c)
                c = 0
            pos += 1
        return bytes(result)

    def _permutate(self, table, block):
        """permute the block with provided table"""
        return list(map(lambda x: block[x], table))

    def _des_crypt(self, block, crypt_type):
        """encrypt or decrypt a data block"""
        block = self._permutate(self.__ip, block)
        num_bits = 8 * self.block_size
        self.L = block[:num_bits // 2]
        self.R = block[num_bits // 2:]

        if crypt_type == self.ENCRYPT:
            key_iter = 0
            key_delt = 1
        else:
            key_iter = 15
            key_delt = -1

        for i in range(0, 16):
            temp_R = self.R
            # expand 32-bit R into 48-bit R
            self.R = self._permutate(self.__expansion_table, self.R)
            self.R = list(map(lambda x, y: x ^ y, self.R, self.Kn[key_iter]))
            B = [self.R[:6], self.R[6:12], self.R[12:18], self.R[18:24],
                 self.R[24:30], self.R[30:36], self.R[36:42], self.R[42:]]

            # permute B[1] to B[8] using the S-boxes
            pos = 0
            Bn = [0] * 32
            for j in range(0, 8):
                # offsets
                m = (B[j][0] << 1) + (B[j][5])
                n = (B[j][1] << 3) + (B[j][2] << 2) + (B[j][3] << 1) + (B[j][4])

                # find the permutation value
                v = self.__sbox[j][(m << 4) + n]

                # turn value into bits
                Bn[pos] = (v & 8) >> 3
                Bn[pos+1] = (v & 4) >> 2
                Bn[pos+2] = (v & 2) >> 1
                Bn[pos+3] = v & 1

                pos += 4

            self.R = self._permutate(self.__p, Bn)

            self.R = list(map(lambda x, y: x ^ y, self.R, self.L))

            self.L = temp_R

            key_iter += key_delt

        self.final = self._permutate(self.__fp, self.R + self.L)
        return self.final

    def _crypt(self, data, crypt_type):
        """split data into blocks and encipher them"""
        # splitting data in blocks, encrypting each one seperately
        i = 0
        result = []

        while i < len(data):
            block = self._string_to_bitlist(data[i:i + self.block_size])
            processed_block = self._des_crypt(block, crypt_type)
            result.append(self._bitlist_to_string(processed_block))
            i += self.block_size

        return b''.join(result)

    def encrypt(self, data):
        """encrypt using ECB mode and PAD_PKCS5"""
        if not data:
            return ''
        data = self._pad_data(data)
        return self._crypt(data, self.ENCRYPT)

    def decrypt(self, data):
        """decrypt using ECB mode and PAD_PKCS5"""
        if not data:
            return ''
        data = self._crypt(data, self.DECRYPT)
        return self._unpad_data(data)
