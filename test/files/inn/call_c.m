inc =
	fun(a) 
	{
		a + 1;
	};
main = 
	fun(a)
	{
		inc(inc(a));
	};