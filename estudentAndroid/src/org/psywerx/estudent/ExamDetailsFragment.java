package org.psywerx.estudent;

import android.app.Fragment;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

public class ExamDetailsFragment extends Fragment {
	
	private TextView v1;
	private TextView v2;
	private TextView v3;
	private TextView v4;
	
	@Override
	public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
		View v = inflater.inflate(R.layout.exam_details_layout, null, false);
		v1 = (TextView) v.findViewById(R.id.textView1);
		v2 = (TextView) v.findViewById(R.id.textView2);
		v3 = (TextView) v.findViewById(R.id.textView3);
		v4 = (TextView) v.findViewById(R.id.textView4);
		
		return v;
	}
	
	public void showData(String v1, String v2, String v3, String v4) {
		this.v1.setText(v1);
		this.v2.setText(v2);
		this.v3.setText(v3);
		this.v4.setText(v4);
	}
}
