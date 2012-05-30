package org.psywerx.estudent;

import java.util.HashMap;

import org.psywerx.estudent.api.Api;
import org.psywerx.estudent.api.ResponseListener;
import org.psywerx.estudent.json.EnrollmentExamDates.EnrollmentExamDate;
import org.psywerx.estudent.json.Signup;

import android.app.Fragment;
import android.app.ProgressDialog;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

public class ExamDetailsFragment extends Fragment implements ResponseListener{
	
	private HashMap<Integer, EditText> data = new HashMap<Integer, EditText>(); 
	private Button btnApplyUnapply;
	
	private ProgressDialog mProgressDialog = null;
	private ResponseListener mListener;
	private String mEnrollmentId;

	private ExamsFragment mExamsFragment;
	private EnrollmentExamDate mExam;
	
	public void setmSignListener(ExamsFragment mSignListener) {
		this.mExamsFragment = mSignListener;
		this.mExam = this.mExamsFragment.mExam;
		this.mEnrollmentId = this.mExamsFragment.mEnrollmentId;
	}
	
	@Override
	public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
		mListener = (ResponseListener) this;
		
		View v = inflater.inflate(R.layout.exam_details_layout, null, false);
		((TextView)v.findViewById(R.id.examID).findViewById(R.id.title)).setText(getString(R.string.examID));
		((TextView)v.findViewById(R.id.examName).findViewById(R.id.title)).setText(getString(R.string.examName));
		((TextView)v.findViewById(R.id.examTeacher).findViewById(R.id.title)).setText(getString(R.string.examTeacher));
		((TextView)v.findViewById(R.id.examDate).findViewById(R.id.title)).setText(getString(R.string.examDate));
		((TextView)v.findViewById(R.id.attempts).findViewById(R.id.title)).setText(getString(R.string.attempts));
		
		data.put(R.id.examID, (EditText)v.findViewById(R.id.examID).findViewById(R.id.description));
		data.put(R.id.examName, (EditText)v.findViewById(R.id.examName).findViewById(R.id.description));
		data.put(R.id.examTeacher, (EditText)v.findViewById(R.id.examTeacher).findViewById(R.id.description));
		data.put(R.id.examDate, (EditText)v.findViewById(R.id.examDate).findViewById(R.id.description));
		data.put(R.id.attempts, (EditText)v.findViewById(R.id.attempts).findViewById(R.id.description));
		
		btnApplyUnapply = (Button)v.findViewById(R.id.btnApplyUnapply);
		btnApplyUnapply.setOnClickListener(new View.OnClickListener() {
			public void onClick(View v) {
				if(signedUp()) {
					mProgressDialog = ProgressDialog.show(getActivity(),    
							getString(R.string.loading_please_wait), 
							getString(R.string.loading_verifying_login), true);
					Api.unapplyExam(mListener, ""+mExam.exam_key, StaticData.username, mEnrollmentId);
				} else {
					mProgressDialog = ProgressDialog.show(getActivity(),    
							getString(R.string.loading_please_wait), 
							getString(R.string.loading_verifying_login), true);
					Api.applyExam(mListener, ""+mExam.exam_key, StaticData.username, mEnrollmentId);
				}
			}
		});
		
		return v;
	}

	public void showData() {
		if (mExam != null){
			//TODO: to ni sifra: 
			data.get(R.id.examID).setText(""+mExam.course_code);
			data.get(R.id.examName).setText(mExam.course);
			data.get(R.id.examTeacher).setText(mExam.instructors);
			data.get(R.id.examDate).setText(mExam.date);
			data.get(R.id.attempts).setText(mExam.all_attempts+"-"+mExam.repeat_class_exams);
			if(signedUp())
				btnApplyUnapply.setText(R.string.unapplyExam);
			else
				btnApplyUnapply.setText(R.string.applyExam);
		}
	}

	public void onServerResponse(Object o) {
		mProgressDialog.dismiss();
		if (o != null && o instanceof Signup) {
			Signup e = (Signup)o;
			if(e.error.isEmpty()) {
				Toast.makeText(getActivity(), e.msg, Toast.LENGTH_LONG).show();
				setSignedUp(!signedUp());
				if(signedUp()) {
					btnApplyUnapply.setText(R.string.unapplyExam);
				} else {
					btnApplyUnapply.setText(R.string.applyExam);
				}
				if(mExamsFragment != null)
					mExamsFragment.reloadData();
			} else {
				Toast.makeText(getActivity(), e.error, Toast.LENGTH_LONG).show();
			}	
		}
	}
	public void setmEnrollmentId(String mEnrollmentId) {
		this.mEnrollmentId = mEnrollmentId;
	}
	
	private boolean signedUp(){
		return mExam != null && mExam.signedup;
	}

	private void setSignedUp(boolean signedup){
		if (mExam != null){
			mExam.signedup = signedup;
		}
	}

	public void setExam(EnrollmentExamDate exam) {
		if (mExamsFragment!=null && mExamsFragment.mExam != null){
			this.mExam = mExamsFragment.mExam;
		} else{
			this.mExam = exam;
		}
	}
}
