package org.psywerx.estudent.extra;

import java.io.UnsupportedEncodingException;
import java.net.URLEncoder;
import java.text.ParseException;
import java.text.SimpleDateFormat;

public class HelperFunctions {
	/**
	 * 
	 * @param args list of all parameter pairs to be encoded (name, value)
	 * @return string of all encoded parameters
	 */
	public static String getFetchParams(String... args){
		String result = "";
		try {
		if (args.length % 2 == 0){
			for (int i=0; i<args.length; i+=2){
				result +=  String.format("%s%s=%s",
						("".equals(result)?"":"&"),
						URLEncoder.encode(args[i],"UTF-8"),
						URLEncoder.encode(args[i+1],"UTF-8")
						);
			}
		}else{
			D.dbge("error encoding url parameters: not enough parameter names");
		}
		}catch (UnsupportedEncodingException e) {
			D.dbge("error encoding url parameteres", e);
		}
		return result;
	}
	
	public static String dateToSlo(String date) {
		try {
			return new SimpleDateFormat("dd.mm.yyyy").format(new SimpleDateFormat("yyyy-mm-dd").parse(date));
		} catch (ParseException e) {
			D.dbge("narobe datum",e);
			return "1.1.2000";
		}
	}
}
