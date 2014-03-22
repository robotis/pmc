"test.mexe" = main in
{{
#"main[f1]" =
[
(Fetch 0)
(CallR #"inc[f1]" 1)
];
#"inc[f1]" =
[
(Fetch 0)
(MakeValP 1)
(CallR #"+[f2]" 2)
];
}}
*
BASIS
;
