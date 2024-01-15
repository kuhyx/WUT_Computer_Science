set Z;
set S; set S1; set S2;
set G1;
set H1;
set P; set P2;
set O2;
set D;
set W;
set N; set Nz; set Nw; set Nzw;

param r{w in W};
param u{i in N, j in N};
param m{p in P, d in D};

var f{i in N, j in N}, >= 0, integer; #a
var a1, >= 0, integer; #e
var a2, >= 0, integer; #f
var a3, >= 0, integer; #g
var a4, >= 0, integer; #h
var bp1, >= 0, integer;
var cp1, >= 0, <=337, integer; #m
var cp2, >= 0, integer;
var co2, >= 0, integer;
var e, >= 0, <=1, integer;
var l, >= 0, integer;

maximize Q: (sum {i in N, w in W} r[w] * f[i,w])
- 10 * (sum {z in Z, s1 in S1} f[z,s1]) - 9 * (sum {z in Z, s2 in S2} f[z,s2])
+ 3 * a1 + 2 * a2 - 2 * a3 - 4 * a4 - 1070 * cp1 - 730 * bp1
- 1500 * (cp2 + co2) - 2 * 200 * l - 43 * (sum {s2 in S2, o2 in O2} f[s2,o2]);

subject to
Ogr_a_c_d{i in N, j in N}:
  f[i,j] <= u[i,j];
Ogr_b{k in Nzw}:
  sum {i in Nz} f[k,i] = sum {j in Nw} f[j,k];    
Ogr_i{z in Z, s1 in S1}:
  a1 <= f[z,s1] - 2056;
Ogr_j{z in Z, s1 in S1}:
  a2 <= f[z,s1] - 4834;
Ogr_k{z in Z, s2 in S2}:
  a3 >= f[z,s2] - 1968;
Ogr_l{z in Z, s2 in S2}:
  a4 >= f[z,s2] - 4417;
Ogr_n: 
  bp1 <= cp1;
Ogr_o{s1 in S1, g1 in G1}:
  cp1 >= f[s1,g1] / 20;
Ogr_p{s1 in S1, h1 in H1}:
  bp1 >= f[s1,h1] / 14;
Ogr_q{s2 in S2, p2 in P2}:
  cp2 >= f[s2,p2] / 25;
Ogr_r: 
  sum {i in N, p in P} f[i,p] <= 13600;
Ogr_s{p in P, d in D}:
  (sum {i in N} f[i,p]) * m[p,d] = f[p,d];
Ogr_t: 
  l >= (sum {i in N, p in P} f[i,p])/200;
Ogr_u{s2 in S2, o2 in O2}:
  co2 >= f[s2,o2] / 25;
Ogr_v{s2 in S2, o2 in O2}:
  f[s2,o2] <= 6000 * e;
Ogr_w{s2 in S2, o2 in O2}:
  f[s2,o2] - 2000 * e >= 0;
Ogr_x{w in W}:
  sum {i in N} f[i,w] >= 4250;
  
solve;
display {i in N, j in N: f[i,j] > 0}: f[i,j];
display: a1; display: a2; display: a3; display: a4; display: bp1;
display: cp1; display: cp2; display: co2; display: 
e; display: l;