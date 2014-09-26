% parses all CSV OptiTrack files in a directory

%Parses all CSV files in directory

files = dir('*.csv');
numfiles = length(files);

clear DATA

for n=1:numfiles
    disp(['Importing ' files(n).name]);
    DATA(n) = importOTdata(files(n).name);
    %Your code here
    %
end