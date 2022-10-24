clc; clear; close;

path(path,'/Users/damaya/Desktop/matlab_scripts/');
path(path,'/Users/damaya/Desktop/matlab_scripts/snctools');
%%
set(0,'DefaultTextFontname', 'CMU Sans Serif')
set(0,'DefaultAxesFontName', 'CMU Sans Serif')

intv=1:1:5000;

% clear fsw
% c=1;
% for k=intv
%     fsw(c)=daily_insolation(k,65,90,2);
%     c=c+1;
% end
Fsw=daily_insolation(intv,65,90,2);

set(gcf,'color','w')
plot(intv,Fsw,'linewidth',2)
ylabel('Insolation @ 65˚N on the Summer Solstice (W m^{-2})')
xlabel('Thousands of years before present')
set(gca,'fontsize',18)
grid

%%
%Example 1: Summer solstice insolation at 65 N')
Fsw=daily_insolation(0:1000,65,90,2);
plot(0:1000,Fsw)
%%
%Example 2: Difference between June 20 (calendar day) and summer solstice insolation at 65 N
june20=datenum(0,6,20)-1; % year 0 is leap-year for datenum'
Fsw1=daily_insolation(0:1000,65,june20);   % June 20')
Fsw2=daily_insolation(0:1000,65,90,2); % solstice')
plot(0:1000,Fsw2);