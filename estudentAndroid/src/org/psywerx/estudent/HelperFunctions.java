package org.psywerx.estudent;

import java.net.URLEncoder;

public class HelperFunctions {
	/**
	 * 
	 * @param args list of all parameter pairs to be encoded (name, value)
	 * @return string of all encoded parameters
	 */
	protected static String getFetchParams(String... args){
		String result = "";
		if (args.length % 2 == 0){
			for (int i=0; i<args.length; i+=2){
				result +=  String.format("%s%s=%s",
						("".equals(result)?"":"&"),
						URLEncoder.encode(args[i]),
						URLEncoder.encode(args[i+1])
						);
			}
		}else{
			D.dbge("error encoding url parameters: not enough parameter names");
		}
		return result;
	}
}
