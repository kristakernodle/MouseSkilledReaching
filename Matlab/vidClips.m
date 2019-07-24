% Grooming and abnormal movement

function [groomingR, groomingTS, abnormR, abnormTS] = vidClips(etNum,vidNum)

%% These are for video 01

switch etNum
    case {'et710','710',710}
        if vidNum == 1
            groomingR = {'R12','R14','R24','R32','R32','R33','R36'};
            groomingTS = [12,0,11,4,10,10,9];
            abnormR = {'R22','R27','R28','R40'};
            abnormTS = [11,15,11,8];
        elseif vidNum == 2
            groomingR = {'R2','R3','R8','R24','R27','R30','R31','R31'};
            groomingTS = [[13,14],[13,16],[12,15],[10,14],[11,14],[4,10],[3,6],[10,14]];
            abnormR = {'R2','R17','R35','R40'};
            abnormTS = [[10,12],[10,11],[10,12],[9,12]];
        elseif vidNum == 3
            disp('No parameters provided')
        end
    case {'et704','704',704}
        if 
end