decr = 
	func(a)
	{
		a - 1;
	};
main = 
	fun(a, b)
	{
		c = a / b + decr(a);
	};