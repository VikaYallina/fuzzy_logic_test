comp(X, XR) :- X < 40, XR = very_low.
comp(X, XR) :- X > 40, XR = very_high.
comp(X, XR) :- X < 40, XR = very_low.
comp(X, XR) :- X > 40, XR = very_high.
comp(X, XR) :- X > 40, XR = very_high.
result(X1,Y,X1R) :- comp(X1, X1R), X1R == very_high, Y = dang.
result(X1,Y,X1R) :- comp(X1, X1R), X1R == very_low, Y = safe.