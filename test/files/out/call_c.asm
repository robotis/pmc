"test.mexe" = main in
{{
#"inc[f1]" =
[
(Fetch 0)
(MakeValP 1)
(CallR #"+[f2]" 2)
];
#"main[f1]" =
[
(Fetch 0)
(Call #"inc[f1]" 1)
(CallR #"inc[f1]" 1)
];
}}
*
BASIS
;
