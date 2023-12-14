%Find and plot the acceptable angles of head tilt to successfully
%administer a drop into the eye. Coordinate system places origin at the
%bottom eyelid. Top of eyelid is p distance above on the positive y axis.
%Bottle tip D is in first quadrant. All points rotate together. Tilts only
%calculated between 0 and 90 degrees.

clearvars
theta_tilt = linspace(0, 90, 10000); %head tilt (degrees). angle of neck extension from the x-axis. 0 tilt is looking straight ahead. Positive tilt is looking up

%variables to change
%define lengths
p = 10; %palpebral fissure height, distance between the lower and upper eyelids (mm)
x = 5; %CHANGE ME. horizontal distance (wrt theta_tilt = 0) from eye to bottle tip.
z = 4; %CHANGE ME. vertical distance (wrt theta_tilt = 0) from center of eye to bottle tip
assert(z >= -p/2) %the eyedrop must be located somewhere on the lens. -p/2 is the lowest it can reasonably be, even with the bottom eyelid

%define angles
theta_d = atand((z+p/2)/x); %neutral angle of point D (degrees)
theta_pb = 0; %angle of point p_b (degrees)
theta_pt = 90; %angle of point p_t (degrees)

%define location of points of interest (r, theta)
D.radius = sqrt(x^2 + (z+p/2)^2); %point d is the location of the eyedrop
D.theta = theta_tilt + theta_d;

Pb.radius = 0;
Pb.theta = theta_tilt + theta_pb;

Pt.radius = p;
Pt.theta = theta_tilt + theta_pt;

%at which theta_tilt values is point D between Pb and Pt?
X_d = D.radius * cosd(D.theta); %x location of point D at different theta tilts
X_pb = Pb.radius * cosd(Pb.theta); %x location of point Pb at different theta tilts
X_pt = Pt.radius * cosd(Pt.theta); %x location of point Pt at different theta tilts

valid_min_idx = find(X_d < X_pb,1); %The first point the bottle tip is above the lower eyelid is a valid drop
if valid_min_idx
    valid_min = theta_tilt(valid_min_idx);
else
    valid_min = theta_tilt(1);
end

valid_max_idx = find(X_d < X_pt,1); %drop is invalid if the bottle tip is past the upper eyelid
if valid_max_idx
    valid_max = theta_tilt(valid_max_idx);
else
    valid_max = theta_tilt(end); %this means the bottle tip is between the upper and lower eyelid, so 90 degree tilt will still be valid
end

%% Plotting
%shaded region is region of valid head tilts.
fs = 15;
lw = 2;
figure;
plot(theta_tilt,X_d,'k','LineWidth',lw);
hold on
plot(theta_tilt,X_pb,'r','LineWidth',lw);
plot(theta_tilt,X_pt,'b','LineWidth',lw);
yl = ylim;
xline(valid_min,'k--','LineWidth',lw)
xline(valid_max,'k--','LineWidth',lw)
x_patch = [valid_min, valid_max, valid_max, valid_min];
y_patch = [yl(1), yl(1), yl(2), yl(2)];
patch(x_patch, y_patch, [.8,.8,.8],'FaceAlpha',.3)

xlabel("Angle of Neck Extension (degrees)",'FontSize',fs)
ylabel("x-axis location of Point of Interest (mm)","FontSize",fs)
grid on
%set(gca, 'XDir','reverse')
legend(["Point D" "Point Pb" "Point Pt"],"FontSize",fs,'Location','southeast')
fprintf("Parameters p: %.2f, x: %.2f, and z: %.2f result in:\n", p, x, z)
fprintf("Min Neck Extension (deg): %.2f\nMax Neck Extension (deg): %.2f\n", valid_min, valid_max)
