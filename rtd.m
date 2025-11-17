rho = 1.06e-7;
t = 100e-9;
Rs = rho / t
w = 60e-6;
Rtarget = 100;
N_squares = Rtarget / Rs
clearance = 35e-6;
pitch = w + clearance;
N = 8;
L_hoz = 550e-6;
L_hoz_total = N * L_hoz
L_vert = pitch;
L_vert_total = (N-1) * pitch
L_ends = 0e-6;
L_eff = L_hoz_total + L_vert_total + L_ends

R_ideal = (rho * L_eff) / (w * t)
Rs_real = Rs * 1.2 % Assuming 30% greater sheet resistance than ideal
N_squares_real = L_eff / w
R_eff = Rs_real * N_squares_real

%% Resistance vs Temperature
R0 = R_eff;               % Your device's nominal resistance at 0°C
A  = 3.9083e-3;
B  = -5.775e-7;
C  = -4.183e-12;          % Only used for T < 0°C

%% --- Temperature range ---
T = -30:0.1:100;          % °C

%% --- Preallocate ---
R_T = zeros(size(T));

%% --- Compute resistance across full temperature range ---
for k = 1:length(T)
    if T(k) >= 0
        % Positive temperatures use: R = R0 * (1 + A*T + B*T^2)
        R_T(k) = R0 * (1 + A*T(k) + B*T(k)^2);
    else
        % Negative temperatures use: R = R0 * [1 + A*T + B*T^2 + C*(T-100)*T^3]
        R_T(k) = R0 * (1 + A*T(k) + B*T(k)^2 + C*(T(k)-100)*(T(k)^3));
    end
end

%% --- Plot ---
figure;
plot(T, R_T, 'LineWidth', 2);
grid on;
xlabel('Temperature (°C)');
ylabel('Resistance (Ω)');
title('Estimated RTD Resistance vs Temperature (Callendar–Van Dusen Model)');