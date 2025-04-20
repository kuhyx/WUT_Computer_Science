library(tmvtnorm)

# t-Stutdet parameters
Mu = c(9, 8, 7, 6)
Sigma = matrix(c(16, -2, -1, -3,
                 -2,  9, -4, -1,
                 -1, -4,  4,  1,
                 -3, -1,  1,  1),
               nrow=4, ncol=4)
lower_bound = 5
upper_bound = 12

# Generate scenarios
data <- rtmvt(n=10000, mean=mu, sigma=sigma, df=5, lower=rep(lower_bound, 4), upper=rep(upper_bound, 4))
write.table(format(data, digits=15, drop0trailing=F), "data10000.txt", quote=F, sep="\t", eol="\n\t", col.names = F, row.names = T)
mean <- colMeans(data)

E <- function(idx, Mu, Sigma, v, alfa, beta) {
  mu = Mu[idx]
  sigma = Sigma[idx, idx]
  a = (alfa - mu)/sigma
  b = (beta - mu)/sigma
  nom = gamma((v-1)/2) *
        ((v+a^2)^(-1*(v-1)/2) - 
         (v+b^2)^(-1*(v-1)/2)) *
        v^(v/2)
  den = 2 * (pt(b, v) - pt(a, v)) * gamma(v/2) * gamma(1/2)
  return (mu + sigma*(nom/den))
}

ER1 <- E(1, Mu, Sigma, 5, 5, 12)
ER2 <- E(2, Mu, Sigma, 5, 5, 12)
ER3 <- E(3, Mu, Sigma, 5, 5, 12)
ER4 <- E(4, Mu, Sigma, 5, 5, 12)
ER <- c(ER1, ER2, ER3, ER4)
write.table(ER, "ER.txt", sep="\t", col.names=F, row.names=F)