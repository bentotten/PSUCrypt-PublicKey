# CS585 Cryptography
# Ben Totten
# My Take on rijndael 

import random  # Future: use system random number generator instead
from functools import partial

primeBits = 33 
numberOfRabinTrials = 40 
seed = 0
# Pre generated primes 
first_primes_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 
                     31, 37, 41, 43, 47, 53, 59, 61, 67,  
                     71, 73, 79, 83, 89, 97, 101, 103,  
                     107, 109, 113, 127, 131, 137, 139,  
                     149, 151, 157, 163, 167, 173, 179,  
                     181, 191, 193, 197, 199, 211, 223, 
                     227, 229, 233, 239, 241, 251, 257, 
                     263, 269, 271, 277, 281, 283, 293, 
                     307, 311, 313, 317, 331, 337, 347, 349]


def main():
    print("~~~ MENU ~~~\n")
    print("\n1) Key Generation\n2) Encryption \n3) Decryption\n")
    selection = input("Input: ")
    
    while selection != "1" and selection != "2" and selection != "3":
        print("\nPlease input option 1, 2, or 3\n")
        selection = input("Input: ")
    
    if selection is "1":
        keygen()
    elif selection is "2":
        encrypt()
    elif selection is "3":
        decrypt()
    else:
        return 1

    return 0


## KEY GENERATION ##
# Select a large prime p (and test for primality)
# Select d in the group {1, ..., p-2} such that 1 <= d <= (p-2)
# Select g to be a primitive root in the group {1, ..., p-1}
# e_2 <- e_1^d mod p
# public_key <- (e_1, e_2, p)
# private_key <- d
# return public_key, private_key
def keygen():
    seed = input("Seed Number: ")
    random.seed(seed)
    
    print("\nGenerating Key\n")
    p = find_prime()
    d = random.randrange(1, (p-2))
    # g = random.randrange(1, (p-1))
    g = 2
    e2 = pow(g, d, p)   # Faster version of (g^d) % p
    
    print("\nPublic Key: ", p, g, e2)
    print("\nPrivate Key: ", p, g, d)
    
    f = open("pubkey.txt", "w")
    f.write(str(p) + " " + str(g) + " " + str(e2))
    f. close()
    
    f = open("prikey.txt", "w")
    f.write(str(p) + " " + str(g) + " " + str(d))
    f.close()


def find_prime():
    print("\nGenerating Prime\n")
    while True:
        primeCandidate = getLowLevelPrime(primeBits)
        if not isMillerRabinPassed(primeCandidate):
            continue
        else:
            return primeCandidate
        

def get_random(bits): 
    return (random.getrandbits(bits))


# Thank you https://www.geeksforgeeks.org/how-to-generate-large-prime-numbers-for-rsa-algorithm/
def getLowLevelPrime(n): 
    while True: 
        # Obtain a random number 
        pc = get_random(n)  
         # Test divisibility by pre-generated  
         # primes 
        for divisor in first_primes_list: 
            if pc % divisor == 0 and divisor**2 <= pc: 
                break
        else: 
            return pc


# Run 40 iterations of Rabin Miller Primality test
def isMillerRabinPassed(mrc): 
    maxDivisionsByTwo = 0
    ec = mrc-1
    while ec % 2 == 0: 
        ec >>= 1
        maxDivisionsByTwo += 1
    assert(2**maxDivisionsByTwo * ec == mrc-1) 
  
    def trialComposite(round_tester): 
        if pow(round_tester, ec, mrc) == 1: 
            return False
        for i in range(maxDivisionsByTwo): 
            if pow(round_tester, 2**i * ec, mrc) == mrc-1: 
                return False
        return True
  
    for i in range(numberOfRabinTrials): 
        round_tester = random.randrange(2, mrc) 
        if trialComposite(round_tester): 
            return False
        i += 1
    return True


def encrypt():

    print("\nEncryption Started\n")
    raw_split = get_pubkey()
    p = int(raw_split[0])
    g = int(raw_split[1])
    e2 = int(raw_split[2])
    
    # LOOP UNTIL END OF FILE! M MUST BE SMALLED THAN P
    cipherfile = open("ctext.txt", "a+")
    with open("ptext.txt") as f:
        block = 1
        while block:
            c2 = [0] * 4
            block = f.read(4)
            if(block):
                msg = list(map(ord, block))   # Convert to ASCII values
            
                result = encryption_math(p, g, e2)

                c1 = result[0]
            
                for i in range(4):
                    c2[i] = (msg[i] * result[1]) % p
            
                print("\nC1: " + str(c1) + "\nC2: " + str(c2))

                cipherfile.write(str(c1) + " " + str(c2) + "\n")
    
    cipherfile.close
            

    
    
def encryption_math(p, g, e2):
    k = random.randrange(1, (p-1))
    x = pow(e2, k, p)
    c1 = pow(g, k, p)
    return [c1, x]
    
    
def get_pubkey():
    f = open("pubkey.txt", "r")
    raw_key = f.read()
    f.close()
    return raw_key.split()




def decrypt():
    print("\nDecryption Started\n")
    

if __name__ == "__main__":
    main()
    