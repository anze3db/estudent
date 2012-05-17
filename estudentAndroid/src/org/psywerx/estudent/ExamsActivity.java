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
		ExamDetailsFragment viewer = (ExamDetailsFragment) getFragmentManager().findFragmentById(R.id.examDetailsFragment);
    	if (viewer == null || !viewer.isInLayout()) {
    		Intent showContent = new Intent(mContext, ExamDetailsActivity.class);
//            showContent.setData(Uri.parse(tutUrl));
            startActivity(showContent);
    	} else {
    		//get data (action = ID od izpita)
    		viewer.showData("Sifra izpita: " + action, "ime: ", "predavatelj: ", "neki: ");
    	}
	}
	
	
}
