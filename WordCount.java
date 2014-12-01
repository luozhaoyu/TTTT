import java.io.IOException;
import java.util.HashMap;
import java.util.StringTokenizer;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.Counter;

import java.net.InetAddress;
import java.util.HashSet;
// Based on http://hadoop.apache.org/docs/r1.2.1/mapred_tutorial.html 
public class WordCount {
	public static class TokenizerMapper extends
			Mapper<Object, Text, Text, IntWritable> {
		private final static IntWritable one = new IntWritable(1);
		private static HashSet<String> allowedWords = new HashSet<String>();
		private static String networkName;
		static {
			String words[] = { "android", "google", "apple", "tech", "java",
					"uber", "amazon", "microsoft", "Motorola", "lenovo",
					"dart", "golang", "java", "javascript", "C", "fortran",
					"ada", "software", "moto360", "samsung", "htc", "dell",
					"hp", "docker", "vine", "twitter", "facebook", "instragram" };
			for (String word : words)
				allowedWords.add(word);
			try {
				networkName = InetAddress.getLocalHost().getHostName();
			} catch (Exception e) {
			}
		}
		private Text word = new Text();

		public void map(Object key, Text value, Context context)
				throws IOException, InterruptedException {
			context.getCounter("MapCount", networkName).increment(1);
			long start = System.currentTimeMillis();
//			System.out.println(value.toString());
			String line = value.toString();
			if(line.contains("<END OF TWEET")){
				context.getCounter("MapLineCount", networkName).increment(1);
			}
			String day;
			try{
			int startOfDate = line.indexOf("| ")+1;
			String date = line.substring(startOfDate,line.indexOf(" |",startOfDate+1));
			int indexOf1stSpace = date.indexOf(" ",1);
			int io2s = date.indexOf(" ",indexOf1stSpace+1);
			int io3s = date.indexOf(" ",io2s+1);
			day = date.substring(1,io3s);
			} catch(IndexOutOfBoundsException e){
				System.err.println("unable to retrieve day from "+line);
				return;
			}
			context.getCounter("MapCount", networkName).increment(1);
			StringTokenizer itr = new StringTokenizer(value.toString());
			Counter counter = context.getCounter("TotalWordCount",day);
			int count =0;
			while (itr.hasMoreTokens()) {
				// String token = itr.nextToken();
				String token = stripNonAlphabeticalChars(itr.nextToken());
				if (allowedWords.contains(token)) {
					word.set(day+": "+token);
					context.write(word, one);
					context.getCounter("TotalTechWordCount",day).increment(1);
				}
				count++;
			}
			counter.increment(count);
			context.getCounter("MapDuration", networkName).increment(
					System.currentTimeMillis() - start);
			// Counters counters = new Counters();
			// Counters.Counter mapDurationCounter =
			// counters.findCounter("group",
			// "mapDuration");
			// context.getCounter("MapDuration",
			// InetAddress.getLocalHost().getHostName()).increment(
			// System.currentTimeMillis() - start);
		}

		// Gets rid of random extra symbols, e.g. #,',.,etc.
		private static String stripNonAlphabeticalChars(String token) {
			StringBuffer word = new StringBuffer();
			for (int i = 0; i < token.length(); i++) {
				char c = token.charAt(i);
				if ((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z')
						|| (c >= '0' && c <= '9')) {
					char x = c;
					if (c >= 'A' && c <= 'Z') {
						x = (char) (c - ('A' - 'a'));
					}
					word.append(c);
				}
			}
			return word.toString();
		}
	}

	public static class IntSumReducer extends
			Reducer<Text, IntWritable, Text, IntWritable> {
		private static String networkName;
		static {
			try {
				networkName = InetAddress.getLocalHost().getHostName();
			} catch (Exception e) {
			}
		}
		private IntWritable result = new IntWritable();

		public void reduce(Text key, Iterable<IntWritable> values,
				Context context) throws IOException, InterruptedException {
			context.getCounter("ReduceCount",
					InetAddress.getLocalHost().getHostName()).increment(1);
			long start = System.currentTimeMillis();
			int sum = 0;
			for (IntWritable val : values) {
				sum += val.get();
			}
			result.set(sum);
			context.write(key, result);
			// Counters counters = new Counters();
			// Counters.Counter reduceDurationCounter =
			// counters.findCounter("group",
			// "reduceDuration");
			context.getCounter("ReduceDuration", networkName).increment(
					System.currentTimeMillis() - start);
		}
	}

	public static void main(String[] args) throws Exception {
		Configuration conf = new Configuration();
		Job job = Job.getInstance(conf, "word count");
		job.setJarByClass(WordCount.class);
		job.setMapperClass(TokenizerMapper.class);
		job.setCombinerClass(IntSumReducer.class);
		job.setReducerClass(IntSumReducer.class);
		job.setOutputKeyClass(Text.class);
		job.setOutputValueClass(IntWritable.class);
		FileInputFormat.addInputPath(job, new Path(args[0]));
		FileOutputFormat.setOutputPath(job, new Path(args[1]));
		System.exit(job.waitForCompletion(true) ? 0 : 1);
	}
}
