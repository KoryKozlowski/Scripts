/*	Author: Kory Kozlowski
 * 	Date: 11/30/2013
 * 	Description: Scans in a file representation of a graph, along with its starting path vertex and 
 * 				 the maximum number of vertexes allowed in the path (essentially cheapest path).
 * 				 The program then calculates the "cheapest path" from the starting vertex to each of
 * 				 the vertices existing within the graph.
 */

import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;

public class ShortestPath {
	public static int INF = Integer.MAX_VALUE;

	public static double[][] shortest(double[][] w1, double[][] w2) {
		double[][] w12 = new double[w1.length][w1.length];
		for (int i = 0; i < w1.length; i++) {
			for (int j = 0; j < w1.length; j++) {
				w12[i][j] = w1[i][j];
				for (int k = 0; k < w1.length; k++) {
					if (w12[i][j] > (w1[i][k] + w2[k][j])) {
						w12[i][j] = w1[i][k] + w2[k][j];
					}
				}
			}
		}
		return w12;
	}

	public static void main(String[] args) throws FileNotFoundException {
		Scanner scan = new Scanner(System.in);
		System.out.println("Please enter filename: ");
		String file = scan.nextLine();
		scan.close();
		File f = new File(file);
		Scanner graph = new Scanner(f);

		// get graph parameters
		int n = graph.nextInt(); 
		int e = graph.nextInt(); 
		int p = graph.nextInt();
		int s = graph.nextInt();

		double[][] result = new double[n][n];
		int v1, v2, m;
		v1 = v2 = m = 0;

		// read in adjacency matrix
		while ((m < e) && (graph.hasNext())) {
			v1 = graph.nextInt() - 1;
			v2 = graph.nextInt() - 1;
			double edge = graph.nextDouble();
			result[v1][v2] = edge;
			result[v2][v1] = edge;
			m++;
		}

		graph.close();
		if ((p < 1) || (p > n)) {
			System.out.print("Invalid Starting Vertex");
			System.exit(0);
		}

		// set non existent edges to INF
		for (int i = 0; i < n; i++) {
			for (int j = 0; j < n; j++) {
				if (result[i][j] == 0) {
					result[i][j] = INF;
				}
			}
			result[i][i] = 0;
		}
		
		if (s > 1) {
			double[][] w1 = new double[n][n];
			double[][] w2 = new double[n][n];
			boolean use1 = false;
			boolean use2 = false;
			for (int i = 0; i < s; i++) {
				if (i == 0) {
					w1 = shortest(result, result);
					use1 = true;
					use2 = false;
				} else if (i == 2) {
					w2 = shortest(w1, w1);
					use1 = false;
					use2 = true;
				} else if (i % 2 == 0) {
					w1 = shortest(w2, w2);
					use1 = true;
					use2 = false;
				} else {
					w2 = shortest(w2, w1);
				}
			}

			for (int i = 0; i < n; i++) {
				if (use1) {
					if (w1[p - 1][i] == INF) {
						System.out.println("INF");
					} else {
						System.out.println(w1[p - 1][i]);
					}
				} else if (use2) {
					if (w2[p - 1][i] == INF) {
						System.out.println("INF");
					} else {
						System.out.println(w2[p - 1][i]);
					}
				}
			}
		}else{
			for(int i = 0; i < n; i++){
				if(result[p-1][i] == INF){
					System.out.println("INF");
				}else{
					System.out.println(result[p-1][i]);
				}
			}
		}

	}
}
