package org.psywerx.estudent.json;


import java.util.List;

public class Index {
	public List<Courses> index;

	public class Courses {
		public List<SingleCourse> courses;
		public float povprecje_izpitov;
		public float povprecje_vaj;
		public float povprecje;
		public String program;
		public int study_year;
		public int lenik;
		public String enrollment_type;
		public boolean redni;

	}


	public class SingleCourse{
		public String sifra_predmeta;
		public String name;
		public String predavatelj;
		public int kreditne_tocke;
		public String datum;
		public int ocena_izpita;
		public int ocena_vaj;
		public int stevilo_polaganj;
		public int odstevek_ponavljanja;
	}

}

