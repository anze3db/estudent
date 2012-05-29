package org.psywerx.estudent;

import java.util.ArrayList;
import java.util.List;

import org.psywerx.estudent.extra.D;
import org.psywerx.estudent.extra.HelperFunctions;
import org.psywerx.estudent.json.EnrollmentExamDates.EnrollmentExamDate;

import android.app.Activity;
import android.app.ListFragment;
import android.content.Context;
import android.os.Bundle;
import android.view.View;
import android.widget.ListView;

public class ExamsFragment extends ListFragment {
	
	private Context mContext;
	
	private MenuAdapter mMenuAdapter;
	private OnExamSelectedListener mExamSelectedListener;
	
	private int mLastPosition = 0;
	
	public interface OnExamSelectedListener {
		public void onExamSelected(int action);
	}
	
	public void reloadData() {
		List<MenuItem> menu = new ArrayList<MenuItem>();
		for(Integer k: StaticData.mEnrollmentExamDates.keySet()) {
			EnrollmentExamDate e = StaticData.mEnrollmentExamDates.get(k);
			if(e.signedup)
				menu.add(new MenuItem(e.course + " (" + e.exam_key + ")", HelperFunctions.dateToSlo(e.date), e.exam_key, R.drawable.check_ok_128));
			else
				menu.add(new MenuItem(e.course + " (" + e.exam_key + ")", HelperFunctions.dateToSlo(e.date), e.exam_key, R.drawable.check_no_128));
		}

		mMenuAdapter = new MenuAdapter(mContext, menu);
		setListAdapter(mMenuAdapter);
		D.dbgv("tuki sm");
	}
	
	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		mContext = getActivity().getApplicationContext();
		
		reloadData();
	}
	
	@Override
	public void onAttach(Activity activity) {
		super.onAttach(activity);
		mExamSelectedListener = (OnExamSelectedListener) activity;
	}
	
	@Override
	public void onListItemClick(ListView l, View v, int position, long id) {
		super.onListItemClick(l, v, position, id);
		
		mLastPosition = position;
		mExamSelectedListener.onExamSelected(mMenuAdapter.getItem(position).getAction());
	}
	
	public void onSign(boolean status) {
		if(status)
			mMenuAdapter.getItem(mLastPosition).addIcon(R.drawable.check_ok_128);
		else
			mMenuAdapter.getItem(mLastPosition).addIcon(R.drawable.check_no_128);
		mMenuAdapter.notifyDataSetChanged();
	}

}
