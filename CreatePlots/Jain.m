function J = Jain(x1,x2)
%calculating Jain fairness index for measurement results x1 and x2

l = min([length(x1),length(x2)]);
J = zeros(l,1);

for i = 1:l
    J(i) = ( (x1(i) + x2(i))^2 ) / ( 2* (x1(i)^2 + (x2(i)^2) ) );
end

end
