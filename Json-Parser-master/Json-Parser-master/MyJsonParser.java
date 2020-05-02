public class MyJsonParser
{
	public static void main(String gg[])
    {
    	JsonP jp=new JsonP("example.txt");
    	boolean flag=jp.validateAndParse();
    	System.out.println(flag);
    	Object value=jp.getValue("five");
    	if (value==null)
    		System.out.println("key not found");
    	else
    		System.out.println(value.toString());
	value = jp.getValueByPath("one/two/three");
	System.out.println(value.toString());		
    }
}
