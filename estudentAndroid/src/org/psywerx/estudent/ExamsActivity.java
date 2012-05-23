package org.psywerx.estudent;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;

public class ExamsActivity extends Activity implements ExamsFragment.OnExamSelectedListener {
	
	private Context mContext;
	
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.exams_fragment);
		
		mContext = getApplicationContext();
	}
	
	public void onExamSelected(int action) {
		//tole je fake. treba popravt (za silo bo)
		String[] data = {""+action, "en ime", "Kodek oO", "1.1.1999"};
		ExamDetailsFragment viewer = (ExamDetailsFragment) getFragmentManager().findFragmentById(R.id.examDetailsFragment);
    	if (viewer == null || !viewer.isInLayout()) {
    		Intent showContent = new Intent(mContext, ExamDetailsActivity.class);
    		showContent.putExtra("id", data[0]);
    		showContent.putExtra("name", data[1]);
    		showContent.putExtra("teacher", data[2]);
    		showContent.putExtra("date", data[3]);
            startActivity(showContent);
    	} else {
    		//get data (action = ID od izpita)
    		viewer.showData(data[0], data[1], data[2], data[3]);
    	}
	}
	
	
}
