import org.apache.commons.codec.digest.DigestUtils;
import java.security.*;

public class Utilities{
	public String static getSHA256hash(String s){
		return DigestUtils.sha256Hex(s);   
	}

	public static String reverseByteHexString(String s) {
		int len = s.length();
		byte[] data = new byte[len / 2];
		for (int i = 0; i < len; i += 2) {
			data[i / 2] = (byte) ((Character.digit(s.charAt(i), 16) << 4)
								 + Character.digit(s.charAt(i+1), 16));
		}
		return new String(data);
	}

}