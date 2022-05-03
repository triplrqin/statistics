clear;
clc;

matrix = importdata('data/Pop Rock.csv');
M = matrix.data(:,2:5);
%M = [matrix.textdata(2:end,4:5), matrix.data(2:end,1)];

% 下面列归一化
v=sum(M);% 列求和
D=diag(v);% 生成以向量v为对角的对角矩阵
R = M*(D^-1);% norm_a即为列归一化矩阵

weights = EntropyWeight(R);

order = M * weights';

matrix.data = [matrix.data,order];

writematrix(matrix.data,'data/The Rolling Stones_matlab.csv');