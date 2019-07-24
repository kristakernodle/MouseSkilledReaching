

directory = '/Volumes/SharedX/Neuro-Leventhal/data/mouseSkilledReaching/et710/DLC/710_20181126/710_20181126_direct/';
frameRate = 59.94;
%% These are for video 01
groomingR = {'R12','R14','R24','R32','R32','R33','R36'};
groomingTS = {[12,14],[0,5],[11,16],[4,6],[10,13],[10,16],[9,16]};

abnormR = {'R22','R27','R28','R40'};
% R27 (abnormTS[2]) - go to end
abnormTS = {[11,14],[15,17],[11,13],[8,10]};

filebase=join({directory,'710_20181126_01_'},'');

% %% These are for video 02
% groomingR = {'R2','R3','R8','R24','R27','R30','R31','R31'};
% groomingTS = [[13,14],[13,16],[12,15],[10,14],[11,14],[4,10],[3,6],[10,14]];
% 
% abnormR = {'R2','R17','R35','R40'};
% abnormTS = [[10,12],[10,11],[10,12],[9,12]];


%% Processing, regardless of video

for reach=1:length(abnormR)
    
    % Define filename
    filebase=join({directory,'710_20181126_01_'},'');
    filebase = join({filebase{1},abnormR{reach}},'');
    sol=dir([filebase{1},'*.csv']);
    filename = join({sol.folder,sol.name},'/');

    % Read in DLC csv file
    [bodyparts,parts_loc,p] = read_DLC_csv(filename{1});
    
    times=abnormTS{reach};
    if times(1) == 0
        times(1) = 1;
    end
    startFrame = floor(times(1)*frameRate);
    endFrame = floor(times(2)*frameRate);
    if endFrame > length(parts_loc(1,:,1))
        endFrame = length(parts_loc(1,:,1));
    end
    numFrames = endFrame - startFrame;
    
    leftPaw = squeeze(parts_loc(1,startFrame:endFrame,:));
    rightPaw = squeeze(parts_loc(2,startFrame:endFrame,:));
    nose = squeeze(parts_loc(3,startFrame:endFrame,:));
    
    leftPaw(:,2) = 1080 - leftPaw(:,2);
    rightPaw(:,2) = 1080 - rightPaw(:,2);
    
    leftPawDist = zeros(length(leftPaw),1);
    rightPawDist = zeros(length(leftPaw),1);
    for pt = 1:length(leftPaw)
        leftPawDist(pt) = pdist([leftPaw(pt,:);nose(pt,:)]);
        rightPawDist(pt) = pdist([rightPaw(pt,:);nose(pt,:)]);
    end
    
    xaxis = times(1):(times(2)-times(1))/numFrames:times(2);
    
    %'visible','off'
    figure('visible','off'); hold on;
    subplot(2,3,1);
        plot(xaxis,leftPaw(:,1));
        title('x position')
        ylabel('Left Paw')
    subplot(2,3,2);
        plot(xaxis,leftPaw(:,2));
        title('y position')
    subplot(2,3,3);
        plot(xaxis,leftPawDist);
        title ('euclidean distance from nose')
    subplot(2,3,4);
        plot(xaxis,rightPaw(:,1),'r');
        ylabel('Right Paw')
        xlabel('time (s)')
    subplot(2,3,5);
        plot(xaxis,rightPaw(:,2),'r');
        xlabel('time (s)')
    subplot(2,3,6);
        plot(xaxis,rightPawDist,'r');
        xlabel('time (s)')
    
    displayNameParts = split(filebase{1},'/');
    displayName = displayNameParts(end);
    displayName = displayName{1};
    displayName = join({displayName, 'Direct View', 'abnormal movement'},', ');
    t = annotation('textbox','String',displayName,'Interpreter','none','EdgeColor','none','FitBoxToText','on');
    t.Position=[0 0 1 1];

    fig = gcf();
    set(fig,'PaperOrientation','landscape','PaperUnits','normalized','PaperPosition',[0 0 1 1]);
    outFilename = join({'/Volumes/SharedX/Neuro-Leventhal/data/mouseSkilledReaching/et710/DLC/710_20181126/xySummaryPlots_direct/',sol.name(1:end-4),'.pdf'},'');
    saveas(fig,outFilename{1})

end


