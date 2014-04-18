"out.mexe" = main in
{{
#"decr[f1]" =
[
(Fetch 0)
(Push)
(MakeVal 1)
(Push)
(CallR #"-[f2]" 2)
];
#"main[f2]" =
[
(Fetch 0)
(Push)
(Fetch 1)
(Push)
(Call #"/[f2]" 2)
(Fetch 0)
(Push)
(Call #"decr[f1]" 1)
(CallR #"+[f2]" 2)
];
}}
*
BASIS
;
