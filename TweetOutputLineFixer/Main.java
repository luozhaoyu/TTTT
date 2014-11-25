import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;

public class Main {

	/**
	 * @param args
	 */
	public static void main(String[] args) throws Exception {
		String filename = args[0];
		StringBuffer output = new StringBuffer();
		BufferedReader reader = new BufferedReader(new FileReader(filename));
		System.out.println("Reading in file...");
		String line = reader.readLine();
		int lineCounter = 0;
		BufferedWriter writer = new BufferedWriter(new FileWriter(filename
				+ "_FIXED"));
		while (line != null) {
			lineCounter++;
			output.append(line);
			if (line.contains("<END OF TWEET")) {
				output.append("\n");
			}
			if (lineCounter % 10000 == 0) {
				System.out.println("Flushing "+lineCounter/10000);
				writeOut(output.toString(), writer);
				output = new StringBuffer();
			}
			line = reader.readLine();
		}
		reader.close();
		// writer.write(output.toString());
		writer.close();
		System.out.println("Done!");
	}

	private static void writeOut(String s, BufferedWriter w) throws Exception {
		w.write(s);
	}
}
