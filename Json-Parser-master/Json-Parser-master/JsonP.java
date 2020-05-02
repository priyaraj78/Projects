import java.util.*;
import java.io.*;
public class JsonP
{
    public static int ptr;
    public static char[] input;
    public String s="";
    public static HashMap<String,String> keys = new HashMap<String,String>();
    public JsonP(String filename)
    {
    	this.input = parseFile(filename);
    }
    private char [] parseFile(String filename)
    {
    	
    	try
		{
			InputStream is=new FileInputStream(filename);
			int size=is.available();
			for (int i=0;i<size;i++)
				s=s+(char)is.read();
			s=s.replace("\n","").replace("\t","").replace("  ","#$#").replace("#$#","");
			//s=s.replace("\t","");
			//s=s.replace(" ","");
			is.close();
		}
		catch(IOException e)
		{
			System.out.println(e.getMessage());
		}

		//System.out.println("Enter the input string:");
		//String s = new Scanner(System.in).nextLine();
  //      s = "{    \"sdf\"  :    234     ,    \"we\":[        11   ,   22]}";
        //s = "{\"sdf\":234,\"we\":[11,22]}";
        return s.toCharArray();
    }
    public static boolean validateAndParse()
    {
    	if(input.length < 1)
        {
            System.out.println("The input string is invalid.");
            return false;
        }
        ptr = 0;
        boolean isValid = object();
        if((isValid) && (ptr == input.length))
        {
            System.out.println("The input json string is valid.");
            return true;
        }
        else
        {
	        traverse();
            System.out.println("The input json string is invalid.");
            return false;
        }
    }
    private static void traverse()
    {
        int x;
        ptr--;
        if(ptr == input.length -1)
        {
            System.out.println("Reached end of file, while parsing");
        }
        else
        {
            if(ptr + 11 < input.length)
            {
                for(x=ptr; x<ptr+11; x++) System.out.print(input[x]);
            }
            else
            {
                for(x=ptr; x<input.length;x++) System.out.print(input[x]);
            }
            System.out.print("\n");
            System.out.println("^\tError");
        }
    }
    private static boolean check()
    {
    	 
    	while(input[ptr] == ' ')
    	{	
    		ptr++;
    		if(ptr>=input.length) {  return false;}
    	}
    	return true;
    }
    private static boolean object()
    {
         
	if(check() == false)
	{
		 
		return false;
	}
        if((input[ptr++] != '{'))
        {
             
            return false;
        }
        if(check() == false)
        {
        	 
        	return false;
        }
		if(ptr>=input.length) { return false;}
        if((input[ptr] =='}'))
        {
            ptr++;
            if(ptr>=input.length) { return false;}
            return true;
        }
        else
        {
            if(member() == false)
            {
                 
                return false;
            }
            if(input[ptr] =='}')
            {
                ptr++;
//				System.out.println(Thread.currentThread().getStackTrace()[2].getMethodName());
				String callerMethodName = "validateAndParse";
				if(callerMethodName.equals(Thread.currentThread().getStackTrace()[2].getMethodName()))
				{
					return true;
				}
            	if(ptr>=input.length) 
                {
                	 
                	return false;
                }
                return true;
            }
        }
        return true;
    }
    
    private static boolean member()
    {
         
        if(pair() == false)
        {
             
            return false;
        }
        else
        {
            if(ptr != input.length-1)
            {
                if(input[ptr++] != ',')
                {
                    ptr--;
                    if (input[ptr]=='}')
                        return true;
                    ptr++;
                    if(ptr>=input.length) { return false;}
                     
                    return false;
                }
                if(ptr>=input.length) { return false;}
                if(check() == false)
                {
                	 
                	return false;
                }
                if(member() == false)
                {
                     
                    return false;
                }
            }
        }
        return true;
    }
    
    private static boolean pair()
    {
         
        if(keyString() == false)
        {
             
            return false;
        }
        if(check() == false)
        {
        	 
        	return false;
        }
        if(input[ptr++] != ':')
        {
             
            return false;
        }
        if(ptr>=input.length) { return false;}
        if(check() == false)
        {
        	 
        	return false;
        }
        if(value() == false)
        {
             
            return false;
        }
        return true;
    }
    private static boolean keyString()
    {
    	 
    	if(input[ptr++] != '"')
    	{
    		 
    		return false;
    	}
    	if(ptr>=input.length) {  return false;}
    	if(keyChars() == false)
    	{
    		 
    		return false;
    	}
    	if(input[ptr++] == '"')
    	{
    		if(ptr>=input.length)
    		{	
    			 
    			return false;
    		}
    		return true;
    	}
    	return false;
    }
    private static boolean keyChars()
    {
    	 
    	String temp=new String("");
    	while(input[ptr] != '"')
    	{
    		temp = temp + input[ptr];
    		ptr++;
    		if(ptr>=input.length)
    		{
    			 
    			return false;
    		}
    	}
    	if(!keys.containsKey(temp))
    	{
    		String keyValue = createValue();
			//System.out.println(keyValue);
            if(keyValue.compareTo("fal") == 0)
            {
                 
                return false;
            }
    		keys.put(temp,keyValue);
    		return true;
    	}
    	else
    	{
    		 
    		System.out.println("Duplicate key :"+ temp);
    		return false;
    	}
    }
    private static String createValue()
    {
        int counter = ptr;
         
	    counter++;
        if(counter >= input.length) {   return "fal";}
        while(input[counter] == ' ')
        {
            counter++;
            if(counter >= input.length) { return "fal";}
        }
        if(input[counter] == ':') counter++;
        if(counter >= input.length) {  return "fal";}
        while(input[counter] == ' ')
        {
            counter++;
            if(counter >= input.length) {   return "fal"; }
        }
        String temp="";
        if(input[counter] == '"')
        {
		counter++;
            if(counter >= input.length) {   return "fal";}
            while(input[counter] != '"')
            {
                temp = temp +input[counter];
                counter++;
                if(counter >= input.length) {  return "fal";}
            }
            return temp;
        }
        if(input[counter] == '{')
        { 
            int countBracket = 1;
            while(countBracket != 0)
            {
                while(input[counter] != '}')
                {
                    temp = temp + input[counter];
                    counter++;
                    if(counter >= input.length) { return "fal";}
                    if(input[counter] == '{') countBracket++;
                }
                temp = temp + input[counter];
                counter ++;
                if(counter >=input.length) {  return "fal";}
                countBracket--;
            }
            return temp;
        }
        if(input[counter] == '[')
        {
            int countBracket = 1;
            while(countBracket != 0)
            {
                while(input[counter] != ']')
                {
                    temp = temp + input[counter];
                    counter++;
                    if(counter >= input.length) {  return "fal";}
                    if(input[counter] == '[') countBracket++;
                }
                temp = temp + input[counter];
                counter ++;
                if(counter >=input.length) {   return "fal";}
                countBracket--;
            }
            return temp;
        }
        if (((input[counter]>='0') && (input[counter]<='9')) || (input[counter] == '-'))
        {
            while(input[counter] != ' ' && input[counter] != ',' && input[counter] != '}' && input[counter] != ']')
            {
                temp = temp + input[counter];
                counter++;
                if(counter >= input.length) {  return "fal"; }
            }
            return temp;
        }
        if ((input[counter]=='t') || (input[counter]=='f') || (input[counter]=='n'))
        {
            int i=0;
    	    if ((input[counter]=='t'))
    	    {
    		    while (i<4)
    		    {
    			    temp+=input[counter];
    			    counter++;
    			    if(counter>=input.length) { return "fal";}
    			    i++;
    		    }
    		    if (temp.compareTo("true")==0)
    			    return temp;
    	    }
    	    if ((input[counter]=='f'))
    	    {
    		    while (i<5)
    		    {
    			    temp+=input[counter];
    			    counter++;
    			    if(counter>=input.length) { return "fal";}
    			    i++;
    		    }
    		    if (temp.compareTo("false")==0)
    			    return temp;
    	    }
    	    if ((input[counter]=='n'))
    	    {
    		    while (i<4)
    		    {
    			    temp+=input[counter];
    			    counter++;
    			    if(counter>=input.length) { return "fal";}
    			    i++;
    		    }
    		    if (temp.compareTo("null")==0)
    			    return temp;
    	    }
        }
        return "";
    }
    private static boolean string()
    {
         
        if(input[ptr++] != '"')
        {
             
            return false;
        }
        if(ptr>=input.length) { return false;}
        if(input[ptr++] == '"')
        {
            return true;
        }
        else
        {
            if(ptr>=input.length) { return false;}
            if(chars() == false)
            {
                 
                return false;
            }
            if(input[ptr++] != '"')
            {
                 
                return false;
            }
            if(ptr>=input.length) { return false;}
        }
        return true;
    }
    
    private static boolean chars()
    {
         
        ptr--;
        while(input[ptr] !='"')
        {
            ptr++;
            if (ptr>=input.length)
            {
                 
            	return false;
            }
        }
        return true;
    }
    
    private static boolean value()
    {
         
        if (input[ptr]=='"')
        {
            if(string() == true)
            {
                return true;
            }
            return false;
        }
        if (input[ptr]=='[')
        {
            if(array() == true)
            {
                return true;
            }
            return false;
        }
        if (input[ptr]=='{')
        {
            if (object() == true)
            {
                return true;
            }
            return false;
        }
        if (((input[ptr]>='0') && (input[ptr]<='9')) || (input[ptr] == '-'))
        {
            if(input[ptr] == '-') ptr++;
		    if(ptr>=input.length) { return false;}
        	if (number() == true)
        	{
        		return true;
        	}
        	return false;
        }
        if ((input[ptr]=='t') || (input[ptr]=='f') || (input[ptr]=='n'))
        {
        	if (bool() == true)
        	{
        		return true;
        	}
        	return false;
        }
        else
        {
            return false;
        }
    }
    
    private static boolean bool()
    {
	 
    	String temp="";
    	int i=0;
    	if ((input[ptr]=='t'))
    	{
    		while (i<4)
    		{
    			temp+=input[ptr];
    			ptr++;
    			if(ptr>=input.length) { return false;}
    			i++;
    		}
    		if (temp.compareTo("true")==0)
    			return true;
    	}
    	if ((input[ptr]=='f'))
    	{
    		while (i<5)
    		{
    			temp+=input[ptr];
    			ptr++;
    			if(ptr>=input.length) { return false;}
    			i++;
    		}
    		if (temp.compareTo("false")==0)
    			return true;
    	}
    	if ((input[ptr]=='n'))
    	{
    		while (i<4)
    		{
    			temp+=input[ptr];
    			ptr++;
    			if(ptr>=input.length) { return false;}
    			i++;
    		}
    		if (temp.compareTo("null")==0)
    			return true;
    	}
    	return false;
    }
    private static boolean number()
    {
         
        if(integer() == false)
        {
             
            return false;
        }
        if(input[ptr] == '.')
        {
            if(fraction() == false)
            {
                 
                return false;
            }
            if(input[ptr] == 'e' || input[ptr] == 'E')
            {
                if(exp() == false)
                {
                     
                    return false;
                }
            }
            return true;
        }
        if(input[ptr] == 'e' || input[ptr] == 'E')
        {
            if(exp() == false)
            {
                 
                return false;
            }
        }
        return true;
    }
    private static boolean exp()
    {
         
        ptr++;
	if(ptr>=input.length) { return false;}
        if(input[ptr] == '+' || input[ptr] =='-')
        {
            ptr++;
	    if(ptr>=input.length) { return false;}
            if(integer() == false)
            {
		 
		return false;
            }
            return true;
        }
        if(integer() == false)
        {
             
            return false;
        }
        return true;
    }
    private static boolean fraction()
    {
         
        if(input[ptr++] != '.')
        {
             
            return false;
        }
	if(ptr>=input.length) { return false;}
        if(input[ptr] == 'e' || input[ptr] == 'E')
        {
             
            return false;
        }
        if(integer() == false)
        {
             
            return false;
        }
        return true;
    }
    private static boolean integer()
    {
	 
    	while ((input[ptr]!=',') && (input[ptr]!='}') && (input[ptr]!=']') && (input[ptr] != '.') && (input[ptr]!='e') && (input[ptr]!='E'))
    	{
    		if ((input[ptr]>='0') && (input[ptr]<='9'))
    		{
    			ptr++;
    			if(ptr>=input.length) { return false;}
    		}
    		else
    		{
    			if(check() == true)
    			{
    				if(input[ptr] == ',') return true;
    			}
    			return false;
    		}
    	}
    	return true;
    }
    
    private static boolean array()
    {
         
        if(input[ptr++] != '[')
        {
             
            return false;
        }
		if(ptr>=input.length) { return false;}
		if(check() == false)
		{
			 
			return false;
		}
        if(input[ptr] ==']')
        {
            ptr++;
            return true;
        }
        else
        {
            if(elements() == false)
            {
                 
                return false;
            }
            if(input[ptr] ==']')
            {
                ptr++;
		if(ptr>=input.length) { return false;}
                return true;
            }
        }
        return true;
    }
    
    private static boolean elements()
    {
         
        if(value() == false)
        {
             
            return false;
        }
        else
        {
                if(input[ptr++] != ',')
                {
		    if(ptr>=input.length) { return false;}
                    ptr--;
                    if (input[ptr]==']')
                        return true;
                    ptr++;
		    if(ptr>=input.length) { return false;}
                     
                    return false;
                }
                if(check() == false)
                {
                	 
                	return false;
                }
                if(elements() == false)
                {
                     
                    return false;
                }
        }
        return true;
    }
    public static Object getValue(String k)
    {
    	return keys.get(k);
    }
    public static Object getValueByPath(String path)
    {
        int flag = 0;
        String errorMessage=new String("");
        String [] paths = path.split("/");
        for(String p : paths)
        {
            if(keys.containsKey(p))
            {
                continue;
            }
            else 
            {
                flag = 1;
                break;
            }
        }
        if(flag == 1)
        {
            errorMessage = errorMessage + "Invalid path.";
            return errorMessage;
        }
        return keys.get(paths[paths.length-1]);
    }
}
/*class JSONObject
{
    private String key;
    private Object value;
    JSONObject(String key, Object value)
    {
        this.key = key;
        this.value = value;
    }
}*/
