import java.security.*;

public class Network{
	public void distribute(){
	}

	public void startNodes(int numNodes){
        KeyPair keyPair = newECKeyPair();
        BCECPrivateKey privateKey = (BCECPrivateKey) keyPair.getPrivate();
        BCECPublicKey publicKey = (BCECPublicKey) keyPair.getPublic();		
	}

	public  KeyPair getNewECKeyPair() throws Exception{
		Security.addProvider(new BouncyCastleProvider());
		KeyPairGenerator keyPairGenerator = KeyPairGenerator.getInstance("ECDSA", BouncyCastleProvider.PROVIDER_NAME);

		ECParameterSpec ecSpec = ECNamedCurveTable.getParameterSpec("secp256k1");
		keyPairGenerator.initialize(ecSpec, new SecureRandom());

		return keyPairGenerator.generateKeyPair();
	}

   public static void main(String args[]){
   }
}