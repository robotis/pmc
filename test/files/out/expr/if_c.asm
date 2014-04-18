"out.mexe" = main in
{{
#"main[f2]" =
[
(Fetch 0)
(Push)
(Fetch 1)
(Push)
(Call #"<[f2]" 2)
(GoTrue _0 0)
(Fetch 0)
(Push)
(MakeVal 1)
(Push)
(Call #">=[f2]" 2)
(GoFalse _0 0)
_2:
(Fetch 0)
(Push)
(MakeVal 1)
(Push)
(Call #"+[f2]" 2)
(Store 0)
(Go _1)
_0:
(Fetch 1)
(Push)
(MakeVal 1)
(Push)
(Call #"+[f2]" 2)
(Store 0)
_1:
(FetchR 0)
];
}}
*
BASIS
;
