"out.mexe" = main in
{{
#"a[f2]" =
[
(MakeVal 12.6)
(Push)
(MakeVal -2)
(Push)
(Fetch 0)
(Push)
(Fetch 1)
(Push)
(Call #"/[f2]" 2)
(Fetch 3)
(Push)
(MakeVal 5)
(Push)
(Call #"*[f2]" 2)
(Call #"+[f2]" 2)
(Fetch 2)
(Push)
(Call #"-[f2]" 2)
(StoreR 2)
];
#"main[f2]" =
[
(MakeVal 12.6)
(Push)
(MakeVal -2)
(Push)
(Fetch 0)
(Push)
(Fetch 1)
(Push)
(Fetch 3)
(Push)
(Call #"+[f2]" 2)
(MakeVal 5)
(Push)
(Call #"*[f2]" 2)
(Call #"/[f2]" 2)
(Fetch 2)
(Push)
(Call #"-[f2]" 2)
(StoreR 2)
];
}}
*
BASIS
;
