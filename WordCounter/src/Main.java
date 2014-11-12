import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.List;

public class Main {

	public static void main(String[] args) {
		if (args.length != 1) {
			System.err
					.println("Takes one input in the form of the WordCount output filename!");
			System.exit(1);
		}
		String inputFile = args[0];
		List<WordCountTuple> tuples = readInFile(inputFile);
		
	}

	private static List<WordCountTuple> readInFile(String outputFile) {
		// StringBuffer output = new StringBuffer();
		List<WordCountTuple> out = new LinkedList<Main.WordCountTuple>();
		BufferedReader reader = null;
		try {
			reader = new BufferedReader(new FileReader(outputFile));
			String line = reader.readLine();
			while (line != null) {
				out.add(new WordCountTuple(
						line.substring(0, line.indexOf('\t')),
						Integer.parseInt(line.substring(line.indexOf('\t') + 1))));
				line = reader.readLine();
			}
		} catch (FileNotFoundException e) {
			System.err.println("Cannot open file " + outputFile);
			e.printStackTrace();
			System.exit(1);
		} catch (IOException e) {
			System.err.println("Cannot read file " + outputFile);
			e.printStackTrace();
			System.exit(1);
		} finally {
			if (reader != null) {
				try {
					reader.close();
				} catch (IOException e) {
					System.err.println("Failed to close reader!");
					e.printStackTrace();
					System.exit(1);
				}
			}
		}
		return out;// put.toString();
	}

	private static class WordCountTuple {
		public int count;
		public String word;

		public WordCountTuple(String word, int count) {
			this.word = word;
			this.count = count;
		}

	}
}
