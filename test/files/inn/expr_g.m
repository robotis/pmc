a = 
	fun(a, b)
	{
		var c = 12.6, d = -2;
		c = a / b + d * 5 - c;
	};
main = 
	fun(a, b)
	{
		var c = 12.6, d = -2;
		c = a / ((b + d) * 5) - c;
	};