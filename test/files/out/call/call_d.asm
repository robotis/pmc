"test.mexe" = main in
{{
#"decr[f1]" =
[
(Fetch 0)
(MakeValP 1)
(CallR #"-[f2]" 2)
];
#"main[f2]" =
[
(Fetch 0)
(FetchP 1)
(Call #"/[f2]" 2)
(FetchP 0)
(Call #"decr[f1]" 1)
(CallR #"+[f2]" 2)
];
}}
*
BASIS
;
