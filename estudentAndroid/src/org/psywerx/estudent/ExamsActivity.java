package org.psywerx.estudent;

import org.psywerx.estudent.extra.D;

import android.app.Activity;
import android.app.FragmentTransaction;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;

public class ExamsActivity extends Activity implements ExamsFragment.OnExamSelectedListener {
	
	private Context mContext;
	private ExamsFragment mViewer;
	private ExamDetailsFragment mDetailsViewer;
	private String mEnrollmentId;
	
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.exams_fragment);

		D.dbgv("starting exams list");
		mViewer = (ExamsFragment) getFragmentManager().findFragmentById(R.id.examsFragment);
		mDetailsViewer = (ExamDetailsFragment) getFragmentManager().findFragmentById(R.id.examDetailsFragment);
		
		mContext = getApplicationContext();
		
		Bundle b = getIntent().getExtras();
		mEnrollmentId = b.getString("enrollment_id");
		mViewer.setmEnrollmentId(mEnrollmentId);
		
		if (mDetailsViewer != null && mDetailsViewer.isInLayout()) {
			mDetailsViewer.setmSignListener(mViewer);
			FragmentTransaction ft = getFragmentManager().beginTransaction();
			ft.hide(mDetailsViewer);
			ft.commit();
		}
		
		if(StaticData.pavzer)
			setTitle(String.format("%s %s (%s) - %s", StaticData.firstName, StaticData.lastName, StaticData.username, getString(R.string.pavzer)));
		else
			setTitle(String.format("%s %s (%s)", StaticData.firstName, StaticData.lastName, StaticData.username));
	}
	
	public void onExamSelected(int action) {
		if (mDetailsViewer == null || !mDetailsViewer.isInLayout()) {
    		Intent showContent = new Intent(mContext, ExamDetailsActivity.class);
    		showContent.putExtra("exam", mViewer.mExam);
    		showContent.putExtra("enroll_id", mEnrollmentId);
            startActivity(showContent);
    	} else if (mDetailsViewer != null){
			mDetailsViewer.setmSignListener(mViewer);
			if(mDetailsViewer.isHidden()) {
				FragmentTransaction ft = getFragmentManager().beginTransaction();
				ft.setCustomAnimations(android.R.animator.fade_in, android.R.animator.fade_out);
				ft.show(mDetailsViewer);
				ft.commit();
			}
    		mDetailsViewer.showData();
    	}
	}
	
	@Override
	protected void onResume() {
		super.onResume();
		mViewer.fetchData();
	}
	
}
