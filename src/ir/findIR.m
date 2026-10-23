clear;clc;
funcDir = getenv('IR_FUNCDIR');
addpath(funcDir);

inputFile = getenv('IR_INPUT');

outputFile = getenv('IR_OUTPUT');
[iRStartPos, iREndPos, iRSeq] = findIR(inputFile, 20, 1000);

fid = fopen(outputFile, 'w');

for i = 1:length(iRStartPos)
    s = iRSeq{i};
    fprintf(fid, '>%d|%d\n', iRStartPos(i), length(s));
    fprintf(fid, '%s\n', s);
end

fclose(fid);
exit;