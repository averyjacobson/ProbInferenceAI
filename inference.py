import random


class Inference:


    #Gibbs sampeling
    def approximateMethod(evidence_B):
        
        #Tunables
        numSamples = 10000
        burnIn = 100

        samples_A = []
        
        # Initialize the variables
        A = random.choice([0, 1])
        B = random.choice([0, 1])

        # Perform Gibbs sampling with burn-in
        for _ in range(numSamples + burnIn):
            # Fix the observed value of B based on evidence
            B = evidence_B

            # Sample A given the current value of B
            P_A_given_B_current = P_A_given_B(B)
            A = 0 if random.random() < P_A_given_B_current else 1

            if _ >= burnIn:
                samples_A.append(A)

        # Estimate the posterior distribution of A
        count_A_0 = samples_A.count(0)
        count_A_1 = samples_A.count(1)

        posterior_A_0 = count_A_0 / (numSamples - burnIn)
        posterior_A_1 = count_A_1 / (numSamples - burnIn)

        return posterior_A_0, posterior_A_1











