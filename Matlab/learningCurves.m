
%% User Defined Variables

% Main directory containing folders named 'et####'
directory = '/Volumes/SharedX/Neuro-Leventhal/data/mouseSkilledReaching/';

%% Get file paths for all .csv score sheets

[filePaths,earTags] = getScoreSheets(directory);

%% Create structure for storing all data

% score = struct('score',[]);
% abmov = struct('abmov',[]);
% groom = struct('groom',[]);
% 
% t1 = struct('T1',{score,abmov,groom});
% t2 = struct('T2',{score,abmov,groom});
% t3 = struct('T3',{score,abmov,groom});
% t4 = struct('T4',{score,abmov,groom});
% t5 = struct('T5',{score,abmov,groom});
% t6 = struct('T6',{score,abmov,groom});
% t7 = struct('T7',{score,abmov,groom});
% t8 = struct('T8',{score,abmov,groom});
% t9 = struct('T9',{score,abmov,groom});
% t10 = struct('T10',{score,abmov,groom});
% t11 = struct('T11',{score,abmov,groom});
% t12 = struct('T12',{score,abmov,groom});
% t13 = struct('T13',{score,abmov,groom});
% t14 = struct('T14',{score,abmov,groom});
% t15 = struct('T15',{score,abmov,groom});
% t16 = struct('T16',{score,abmov,groom});
% t17 = struct('T17',{score,abmov,groom});
% t18 = struct('T18',{score,abmov,groom});
% t19 = struct('T19',{score,abmov,groom});
% t20 = struct('T20',{score,abmov,groom});
% t21 = struct('T21',{score,abmov,groom});

et704 = struct('name','et704','box','2','pawPref','left','genotype','WT',...
    'T1',[],'T2',[],'T3',[],'T4',[],'T5',[],'T6',[],'T7',[],'T8',[],...
    'T9',[],'T10',[],'T11',[],'T12',[],'T13',[],'T14',[],'T15',[],...
    'T16',[],'T17',[],'T18',[],'T19',[],'T20',[],'T21',[]);

et710 = struct('name','et710','box','1','pawPref','right','genotype','KO',...
    'T1',[],'T2',[],'T3',[],'T4',[],'T5',[],'T6',[],'T7',[],'T8',[],...
    'T9',[],'T10',[],'T11',[],'T12',[],'T13',[],'T14',[],'T15',[],...
    'T16',[],'T17',[],'T18',[],'T19',[],'T20',[],'T21',[]);

et713 = struct('name','et713','box','1','pawPref','right','genotype','WT',...
    'T1',[],'T2',[],'T3',[],'T4',[],'T5',[],'T6',[],'T7',[],'T8',[],...
    'T9',[],'T10',[],'T11',[],'T12',[],'T13',[],'T14',[],'T15',[],...
    'T16',[],'T17',[],'T18',[],'T19',[],'T20',[],'T21',[]);

et717 = struct('name','et717','box','2','pawPref','right','genotype','KO',...
    'T1',[],'T2',[],'T3',[],'T4',[],'T5',[],'T6',[],'T7',[],'T8',[],...
    'T9',[],'T10',[],'T11',[],'T12',[],'T13',[],'T14',[],'T15',[],...
    'T16',[],'T17',[],'T18',[],'T19',[],'T20',[],'T21',[]);

et719 = struct('name','et719','box','1','pawPref','right','genotype','KO',...
    'T1',[],'T2',[],'T3',[],'T4',[],'T5',[],'T6',[],'T7',[],'T8',[],...
    'T9',[],'T10',[],'T11',[],'T12',[],'T13',[],'T14',[],'T15',[],...
    'T16',[],'T17',[],'T18',[],'T19',[],'T20',[],'T21',[]);

et740 = struct('name','et740','box','2','pawPref','left','genotype','WT',...
    'T1',[],'T2',[],'T3',[],'T4',[],'T5',[],'T6',[],'T7',[],'T8',[],...
    'T9',[],'T10',[],'T11',[],'T12',[],'T13',[],'T14',[],'T15',[],...
    'T16',[],'T17',[],'T18',[],'T19',[],'T20',[],'T21',[]);

et743 = struct('name','et743','box','2','pawPref','left','genotype','WT',...
    'T1',[],'T2',[],'T3',[],'T4',[],'T5',[],'T6',[],'T7',[],'T8',[],...
    'T9',[],'T10',[],'T11',[],'T12',[],'T13',[],'T14',[],'T15',[],...
    'T16',[],'T17',[],'T18',[],'T19',[],'T20',[],'T21',[]);

et745 = struct('name','et745','box','1','pawPref','left','genotype','KO',...
    'T1',[],'T2',[],'T3',[],'T4',[],'T5',[],'T6',[],'T7',[],'T8',[],...
    'T9',[],'T10',[],'T11',[],'T12',[],'T13',[],'T14',[],'T15',[],...
    'T16',[],'T17',[],'T18',[],'T19',[],'T20',[],'T21',[]);

et749 = struct('name','et749','box','1','pawPref','left','genotype','WT',...
    'T1',[],'T2',[],'T3',[],'T4',[],'T5',[],'T6',[],'T7',[],'T8',[],...
    'T9',[],'T10',[],'T11',[],'T12',[],'T13',[],'T14',[],'T15',[],...
    'T16',[],'T17',[],'T18',[],'T19',[],'T20',[],'T21',[]);

% et7061 = struct('et7061',{t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t11,t12,t13,t14,t15,t16,t17,t18,t19,t20,t21});
% et7062 = struct('et7062',{t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t11,t12,t13,t14,t15,t16,t17,t18,t19,t20,t21});
% et7063 = struct('et7063',{t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t11,t12,t13,t14,t15,t16,t17,t18,t19,t20,t21});
% et7064 = struct('et7064',{t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t11,t12,t13,t14,t15,t16,t17,t18,t19,t20,t21});
% et7065 = struct('et7065',{t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t11,t12,t13,t14,t15,t16,t17,t18,t19,t20,t21});
% et7068 = struct('et7068',{t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t11,t12,t13,t14,t15,t16,t17,t18,t19,t20,t21});
% et7076 = struct('et7076',{t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t11,t12,t13,t14,t15,t16,t17,t18,t19,t20,t21});

allData = {et704,et710,et713,et717,et719,et740,et743,et745,et749}; %et7061,et7062,et7063,et7064,et7065,et7068,et7076

%% Read .csv data into allData (data structure)

for ii = 1:length(filePaths)
    filename = filePaths(ii);
    
    pathParts = split(filename,'/');
    sessionID = pathParts(end-1);
    
    sessionParts = split(sessionID,'_');
    
    for jj = 1:length(allData)
        if strcmp(allData{jj}.name,sessionParts(1))
            etIdx = jj;
            break;
        end
    end
    
    csv = csvread(filename,2);
    
    allData{jj} = setfield(allData{jj},sessionParts(end),'score',csv(:,2)
    
    
    
    
end

