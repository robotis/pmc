decr = 
	fun(a)
	{
		a - 1;
	};
main = 
	fun(a, b)
	{
		var c = a / b + decr(a);
	};