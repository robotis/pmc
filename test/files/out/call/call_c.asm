"out.mexe" = main in
{{
#"inc[f1]" =
[
(Fetch 0)
(Push)
(MakeVal 1)
(Push)
(CallR #"+[f2]" 2)
];
#"main[f1]" =
[
(Fetch 0)
(Push)
(Call #"inc[f1]" 1)
(CallR #"inc[f1]" 1)
];
}}
*
BASIS
;
