clear;clc;
funcDir = getenv('IR_FUNCDIR');
addpath(funcDir);

%% Input.
inputFile =  getenv('IR_INPUT');

%% Output
perfOut = getenv('IR_PERF_OUT');
perfRun = getenv('IR_PERF_RUN');
imperfOut = getenv('IR_IMPERF_OUT');
imperfRun = getenv('IR_IMPERF_RUN');

Data = fastaread(inputFile);
seq  = Data.Sequence;

%% ---------- Perfect detection ----------
tic;
[startPos, endPos, irSeq] = detectPerfectIR(seq, 10, 1000);
runtime = toc;

irNumber = 0;
for i = 1:length(startPos)
    irNumber = irNumber + length(startPos{i});
end

fid = fopen(perfRun, 'a');
fprintf(fid, '-------%s-------\n', perfOut);
fprintf(fid, 'IR Numbers: %d\n', irNumber);
fprintf(fid, 'Runtime: %f s\n', runtime);
fclose(fid);

fid = fopen(perfOut, 'w');
for i = 1:length(startPos)
    for j = 1:length(startPos{i})
        if iscell(irSeq{i})
            s = irSeq{i}{j};
        else
            s = irSeq{i}(j, :);
        end
        fprintf(fid, '>%d|%d\n', startPos{i}(j), length(s));
        fprintf(fid, '%s\n', s);
    end
end
fclose(fid);

%% ---------- Imperfect detection ----------
tic;
[startPos, misMatchNum, irSeq] = detectImperfectIR(seq, 20, 1000, 6);
runtime = toc;

irNumber = 0;
for i = 1:length(startPos)
    irNumber = irNumber + length(startPos{i});
end

fid = fopen(imperfRun, 'a');
fprintf(fid, '-------%s-------\n', imperfOut);
fprintf(fid, 'IR Numbers: %d\n', irNumber);
fprintf(fid, 'Runtime: %f s\n', runtime);
fclose(fid);

fid = fopen(imperfOut, 'w');
for i = 1:length(startPos)
    for j = 1:length(startPos{i})
        if iscell(irSeq{i})
            s = irSeq{i}{j};
        else
            s = irSeq{i}(j, :);
        end
        fprintf(fid, '>%d|%d\n', startPos{i}(j), length(s));
        fprintf(fid, '%s\n', s);
    end
end
fclose(fid);
exit;