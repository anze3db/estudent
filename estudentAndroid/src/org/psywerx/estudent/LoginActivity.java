package org.psywerx.estudent;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

public class LoginActivity extends Activity {
	
	private Context mContext;
	
	private EditText mEditUsername;
	private EditText mEditPassword;
	private Button mBtnConfirm;
	
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.login_layout);
        mContext = getApplicationContext();
        
        init();
        setListeners();
    }
    
	private void init() {
		mEditUsername = (EditText) findViewById(R.id.eUsername);
		mEditPassword = (EditText) findViewById(R.id.ePassword);
		mBtnConfirm = (Button) findViewById(R.id.btnConfirm);
	}
	
	private void setListeners(){
		mBtnConfirm.setOnClickListener(new View.OnClickListener() {
			public void onClick(View v) {
				String username = mEditUsername.getText().toString();
				String password = mEditPassword.getText().toString();
				if (username.length() == 0) {
					mEditUsername.setError(getText(R.string.error_required));
					mEditUsername.requestFocus();
					return;
				}
				if (password.length() == 0) {
					mEditPassword.setError(getText(R.string.error_required));
					mEditPassword.requestFocus();
					return;
				}
				//Api.loginRequest(mListener, username, password);
				//TODO
				Intent intent = new Intent(mContext, MenuActivity.class);
				startActivity(intent);
			}
		});
	}
	
	@Override
	protected void onResume() {
		super.onResume();
		mEditUsername.setText("");
		mEditUsername.requestFocus();
		mEditPassword.setText("");
	}
}