"test.mexe" = main in
{{
#"a[f2]" =
[
(MakeVal 12.6)
(MakeValP -2)
(FetchP 0)
(FetchP 1)
(Call #"/[f2]" 2)
(FetchP 3)
(MakeValP 5)
(Call #"*[f2]" 2)
(Call #"+[f2]" 2)
(FetchP 2)
(Call #"-[f2]" 2)
(StoreR 2)
];
#"main[f2]" =
[
(MakeVal 12.6)
(MakeValP -2)
(FetchP 0)
(FetchP 1)
(FetchP 3)
(Call #"+[f2]" 2)
(MakeValP 5)
(Call #"*[f2]" 2)
(Call #"/[f2]" 2)
(FetchP 2)
(Call #"-[f2]" 2)
(StoreR 2)
];
}}
*
BASIS
;
