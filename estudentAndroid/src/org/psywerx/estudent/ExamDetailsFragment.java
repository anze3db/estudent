package org.psywerx.estudent;

import java.util.HashMap;

import android.app.Fragment;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.EditText;
import android.widget.TextView;

public class ExamDetailsFragment extends Fragment {
	
	private HashMap<Integer, EditText> data = new HashMap<Integer, EditText>(); 
	
	@Override
	public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
		View v = inflater.inflate(R.layout.exam_details_layout, null, false);
		((TextView)v.findViewById(R.id.examID).findViewById(R.id.title)).setText(getString(R.string.examID));
		((TextView)v.findViewById(R.id.examName).findViewById(R.id.title)).setText(getString(R.string.examName));
		((TextView)v.findViewById(R.id.examTeacher).findViewById(R.id.title)).setText(getString(R.string.examTeacher));
		((TextView)v.findViewById(R.id.examDate).findViewById(R.id.title)).setText(getString(R.string.examDate));
		
		data.put(R.id.examID, (EditText)v.findViewById(R.id.examID).findViewById(R.id.description));
		data.put(R.id.examName, (EditText)v.findViewById(R.id.examName).findViewById(R.id.description));
		data.put(R.id.examTeacher, (EditText)v.findViewById(R.id.examTeacher).findViewById(R.id.description));
		data.put(R.id.examDate, (EditText)v.findViewById(R.id.examDate).findViewById(R.id.description));
		
		return v;
	}
	
	public void showData(String id, String name, String teacher, String date) {
		data.get(R.id.examID).setText(id);
		data.get(R.id.examName).setText(name);
		data.get(R.id.examTeacher).setText(teacher);
		data.get(R.id.examDate).setText(date);
	}
}
