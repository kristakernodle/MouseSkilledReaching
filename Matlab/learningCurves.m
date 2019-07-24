
% 
directory = '/Volumes/SharedX/Neuro-Leventhal/data/mouseSkilledReaching/';

earTags = {};
trainingDays = {};


folders = dir(directory);
for ii = 1:length(folders)
    if folders(ii).isdir == 1 && ~isempty(strfind(folders(ii).name,'et'))
        earTags{end+1} = folders(ii).name;
    end
end

for ii = 1:length(earTags)
    
    trainDir = strcat(directory,earTags{ii},'/Training/');
    
    folders = dir(presDir);
    for jj = 1:length(folders)
        if folders(jj).isdir == 1 && ~isempty(strfind(folders(jj).name,earTags{ii}))
            trainingDays{end+1} = folders(jj).name;
        end
    end % for jj = 1:length(folders=dir(presDir))
    
    for jj = 1:length(trainingDays)
        
        dayDir = strcat(trainDir,trainingDays{jj},'/');
        files = dir(dayDir);
        for kk = 1:length(files)
            if files(kk).isdir == 0 && ~isempty(strfind(files(kk).name,'Scored.csv'))
                disp(files(kk).name)
                
                
            end
        end % for kk = 1:length(files=dir(dayDir))
        
        
    end % for jj = 1:length(trainingDays)
    
end % for ii = 1:length(earTags)