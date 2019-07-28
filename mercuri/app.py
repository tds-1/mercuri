from flask import Flask, render_template, request, redirect, jsonify, make_response
import flask
import random
import queue
import sqlite3 as sql
app = Flask(__name__, static_folder="static_dir")

# # debug mode on
# if __name__ == "__main__":
# 	app.run(debug=True)

def resetdb():
	with sql.connect("hack.db") as con:
		cur=con.cursor()
		cur.execute("delete from bucket1")
		cur.execute("delete from bucket2")
		cur.execute("delete from savedata")
		cur.execute("delete from bucket3")
		cur.execute("update user_rating set rating=1500")
		cur.execute("update problem set rating=1500")
		cur.execute("INSERT INTO bucket1 select problem_id, course_id from problem")
	con.close()
resetdb()

def tellpid(title,cid):
	z=1
	with sql.connect("hack.db") as con:
		cur=con.cursor()
		cur.execute("select problem_id from problem where title=(?) and course_id=(?)",[title,cid])
		z=cur.fetchone()[0]
		con.commit()
	con.close()
	return z

def set_dependency(cid):
	mp={}
	with sql.connect("hack.db") as con:
		cur=con.cursor()
		x=list(cur.execute("select problem_id from problem where course_id=(?)",[cid]))
		for i in x:
			# print(i[0])
			mp[i[0]]=[]
		vec=list(cur.execute("select distinct * from dependencies where course_id=(?)",[cid]))
		for i in vec:
			mp[tellpid(i[1],cid)].append(tellpid(i[0],cid))
		# print("mmmmmmmmmmmpppppppppppppp->",mp)
		con.commit()
	con.close()
	return mp

@app.route("/entry", methods=["GET"])
def fun_get():
	print("here")
	s={}
	with sql.connect("hack.db") as con:
		cur=con.cursor()
		cur.execute("select course_name,course_id from course")
		for row in cur:  
			c=0
			st=""
			f=0
			for x in row:
				if(c%2==0):
					st=x
				else:
					f=x
				c+=1
				s[st]=x	
		con.commit()
	con.close()
	return render_template("index.html",msg=s)

@app.route("/entry", methods=["POST"])
def func_post():
	print ("in 2")
	topic=request.args.get('id')
	topic=str(topic)
	print (topic)
	s=[]
	s.clear()
	rowid = None
	with sql.connect("hack.db") as con:
		cur=con.cursor()
		cur.execute("INSERT INTO course (course_name) VALUES (?)",[topic])
		con.commit()
		row = cur.execute("SELECT * FROM course where course_id = (?)" , [cur.lastrowid]).fetchone()
	con.close()
	return jsonify({'course_id': row[0], 'course_name': row[1]})

@app.route("/entry", methods=["DELETE"])
def func_del():
	print ("in 3")
	ss=request.args.get('id')
	print ("from DELETE-> "+ss)
	with sql.connect("hack.db") as con:
		cur=con.cursor()
		cur.execute("Select distinct course.course_id from course join problem on problem.course_id= course.course_id where course_name=(?)",[ss])
		cid=cur.fetchone()	
		try:
			cid=(cur.fetchone()[0])
		except:
			cid=0
		print ("delete --> ",cid)
		cur.execute("DELETE From course where course_name=(?)",[ss])
		cur.execute("DELETE From problem where course_id=(?)",[cid])

		con.commit()
	con.close()
	j=1
	s={}
	with sql.connect("hack.db") as con:
		cur=con.cursor()
		cur.execute("select course_name,course_id from course")
		for row in cur:  
			c=0
			f=0
			for x in row:
				if(c%2==0):
					st=x
				else:
					f=x
				c+=1
				s[st]=x	
		con.commit()
	con.close()
	# print (s)
	return render_template("index.html",msg=s)

@app.route("/course/<variable>", methods=["GET"])
def fun_course(variable):
	print ("course --> "+variable)
	s={}
	c_name=variable.replace('-',' ')
	cid=1
	with sql.connect("hack.db") as con:
		curr=con.cursor()
		curr.execute("SELECT course_id FROM course WHERE course_name= (?)",[c_name])
		cid= (curr.fetchone()[0])
		con.commit()
	con.close()

	s1=[]
	s2=[]
	s3=[]
	with sql.connect("hack.db") as con:
		cur=con.cursor()
		cur.execute("select distinct title from problem where course_id=(?) and type=1",[cid])
		s=cur.fetchall()
		for var in s:
			s1.append(var[0])
		cur.execute("select distinct title from problem where course_id=(?) and type=2",[cid])
		s=cur.fetchall()
		for var in s:
			s2.append(var[0])
		cur.execute("select distinct title from problem where course_id=(?) and type=3",[cid])
		s=cur.fetchall()
		for var in s:
			s3.append(var[0])
		con.commit()
	con.close()
	print (s1,s2,s3)
	return render_template("course.html",cn=variable, msg1=s1, msg2=s2, msg3=s3)

@app.route("/course/<variable>", methods=["POST"])
def fun_cpost(variable):
	c_name=variable.replace('-',' ')
	flag=0
	try:
		try:
			img1=request.form["pic1"]
			with sql.connect("hack.db") as con:
				cur=con.cursor()
				cur.execute("update course set img1=(?) where course_name=(?)",[img1,c_name])
				con.commit()
			con.close()
			flag=1
		except:
			try:
				img2=request.form["pic2"]
				with sql.connect("hack.db") as con:
					cur=con.cursor()
					cur.execute("update course set img2=(?) where course_name=(?)",[img2,c_name])
					con.commit()
				con.close()
				flag=1
			except:
				img3=request.form["pic3"]
				with sql.connect("hack.db") as con:
					cur=con.cursor()
					cur.execute("update course set img3=(?) where course_name=(?)",[img3,c_name])
					con.commit()
				con.close()
				flag=1
	except:
		flag=0
	if (flag==1):
		cid=1
		with sql.connect("hack.db") as con:
			curr=con.cursor()
			curr.execute("SELECT course_id FROM course WHERE course_name= (?)",[c_name])
			cid= (curr.fetchone()[0])
			con.commit()
		con.close()

		s1=[]
		s2=[]
		s3=[]
		with sql.connect("hack.db") as con:
			cur=con.cursor()
			cur.execute("select distinct title from problem where course_id=(?) and type=1",[cid])
			s=cur.fetchall()
			for var in s:
				s1.append(var[0])
			cur.execute("select distinct title from problem where course_id=(?) and type=2",[cid])
			s=cur.fetchall()
			for var in s:
				s2.append(var[0])
			cur.execute("select distinct title from problem where course_id=(?) and type=3",[cid])
			s=cur.fetchall()
			for var in s:
				s3.append(var[0])
			con.commit()
		con.close()
		print (s1,s2,s3)
		return render_template("course.html",cn=variable, msg1=s1, msg2=s2, msg3=s3)


	try:	
		title=request.form["title1"]
		problem=request.form["problem1"]
		canswer=request.form["opt11"]
		wanswer1=request.form["opt21"]
		wanswer2=request.form["opt31"]
		wanswer3=request.form["opt41"]
		correct_opt=request.form["option1"]
		typ=1
	except:
		try:
			title=request.form["title2"]
			problem=request.form["problem2"]
			canswer=request.form["opt12"]
			wanswer1=request.form["opt22"]
			wanswer2=request.form["opt32"]
			wanswer3=request.form["opt42"]
			correct_opt=request.form["option2"]
			typ=2
		except:
			title=request.form["title3"]
			problem=request.form["problem3"]
			canswer=request.form["opt13"]
			wanswer1=request.form["opt23"]
			wanswer2=request.form["opt33"]
			wanswer3=request.form["opt43"]
			correct_opt=request.form["option3"]
			typ=3 
	print ("title--> "+title)
	c_name=variable.replace('-',' ')
	cid=1
	with sql.connect("hack.db") as con:
		cur=con.cursor()
		cur.execute("SELECT course_id FROM course WHERE course_name= (?)",[c_name])
		cid= (cur.fetchone()[0])
		cur.execute("INSERT INTO problem (title,problem,canswer,wanswer1,wanswer2,wanswer3,course_id,correct_opt,type) VALUES (?,?,?,?,?,?,?,?,?)",[title,problem,canswer,wanswer1,wanswer2,wanswer3,cid,correct_opt,typ])
		con.commit()
	con.close()
	s1=[]
	s2=[]
	s3=[]
	with sql.connect("hack.db") as con:
		cur=con.cursor()
		cur.execute("select distinct title from problem where course_id=(?) and type=1",[cid])
		s=cur.fetchall()
		for var in s:
			s1.append(var[0])
		cur.execute("select distinct title from problem where course_id=(?) and type=2",[cid])
		s=cur.fetchall()
		for var in s:
			s2.append(var[0])
		cur.execute("select distinct title from problem where course_id=(?) and type=3",[cid])
		s=cur.fetchall()
		for var in s:
			s3.append(var[0])
		con.commit()
	con.close()
	with sql.connect("hack.db") as con:
		cur=con.cursor()
		cur.execute("SELECT problem_id FROM problem WHERE title= (?)",[title])
		pid= (cur.fetchone()[0])
		cur.execute("insert into bucket1 VALUES (?,?)",(pid,cid))
		con.commit()
	con.close()
	print (s1,s2,s3)
	return render_template("course.html",cn=variable, msg1=s1, msg2=s2, msg3=s3)

@app.route("/course/<variable>", methods=["DELETE"])
def cdelete(variable):
	c_name=variable.replace('-',' ')
	ss=request.form['id']
	print ("title -->",id)
	##DELETE A PROBLEM FROM DB
	cid=0
	with sql.connect("hack.db") as con:
		cur=con.cursor()
		cur.execute("delete from bucket1 where bucket1.problem_id in (select problem_id from problem JOIN course ON problem.course_id=course.course_id where course_name=(?) and title=(?))",(c_name,ss))
		cur.execute("delete from bucket2 where bucket2.problem_id in (select problem_id from problem JOIN course ON problem.course_id=course.course_id where course_name=(?) and title=(?))",(c_name,ss))
		cur.execute("delete from bucket3 where bucket3.problem_id in (select problem_id from problem JOIN course ON problem.course_id=course.course_id where course_name=(?) and title=(?))",(c_name,ss))
		cur.execute("SELECT course_id FROM course WHERE course_name= (?)",[c_name])
		cid= (cur.fetchone()[0])
		cur.execute("delete from problem where course_id=(?) and title=(?)",[cid,ss])
		con.commit()
	con.close()
	j=1
	s1=[]
	s2=[]
	s3=[]
	print ("cid-->",cid)
	with sql.connect("hack.db") as con:
		cur=con.cursor()
		cur.execute("select distinct title from problem where course_id=(?) and type=1",[cid])
		s=cur.fetchall()
		for var in s:
			s1.append(var[0])
		cur.execute("select distinct title from problem where course_id=(?) and type=2",[cid])
		s=cur.fetchall()
		for var in s:
			s2.append(var[0])
		cur.execute("select distinct title from problem where course_id=(?) and type=3",[cid])
		s=cur.fetchall()
		for var in s:
			s3.append(var[0])
		con.commit()
	con.close()
	print (s1,s2,s3)
	return render_template("course.html",cn=variable, msg1=s1, msg2=s2, msg3=s3)

@app.route("/problem/<variable>", methods=["GET"])
def display(variable):
	print ("varr--> "+ variable)
	c_name=variable.replace('-',' ')
	cid=[]
	with sql.connect("hack.db") as con:
		cur=con.cursor()
		cur.execute("SELECT * FROM problem WHERE title= (?)",[c_name])
		cid= (cur.fetchone())
		con.commit()
	con.close()	
	print (cid)
	return render_template("question_display.html",title=cid[1],problem=cid[2], ca=cid[3], cw1=cid[4], cw2=cid[5], cw3=cid[6])
type1=[]
type2=[]
type3=[]
	
@app.route("/course/<variable>/preview-course", methods=["GET"])
def preview(variable):
	c_name=variable.replace('-',' ')
	print("coursname-->"+c_name)
	resetdb()
	type1.clear()
	type2.clear()
	type3.clear()
	cid=1
	with sql.connect("hack.db") as con:
		cur=con.cursor()
		cur.execute("SELECT course_id FROM course WHERE course_name= (?)",[c_name])
		cid=cur.fetchone()[0]
		cur.execute("SELECT problem_id FROM problem WHERE course_id= (?) and type=1",[cid])
		x=cur.fetchall()
		for i in x:
			type1.append(i[0])
		random.shuffle(type1)

		cur.execute("INSERT into savedata VALUES (?)",[type1[0]])
		cur.execute("INSERT into progress VALUES (1,0)")
	con.close()
	print(type1,type2,type3)
	c_id=cid
	cid=[]
	with sql.connect("hack.db") as con:
		cur=con.cursor()
		cur.execute("SELECT * FROM problem WHERE course_id= (?) and type=1",[c_id])
		x=list(cur.fetchall()[0])
		for i in x:
			cid.append(i)
		cur.execute("update progress set stage=1")
	con.close()

	return render_template("preview.html",name=variable,title=cid[1],problem=cid[2], ca=cid[3], cw1=cid[4], cw2=cid[5], cw3=cid[6])


@app.route("/course/<variable>/preview-course", methods=["POST"])
def prev_pos(variable):
	c_name=variable.replace('-',' ')
	c_id=0;
	with sql.connect("hack.db") as con:			#finding the course
		cur=con.cursor()
		cur.execute("select course_id from course where course_name=(?)",[c_name])
		c_id=(cur.fetchone()[0])
		con.commit()
	con.close()
	
	try:
		submi=str(request.form['select'])
	except:
		cid=[]
		with sql.connect("hack.db") as con:
			cur=con.cursor()
			cur.execute("select present from savedata")
			x=cur.fetchone()[0]
			print (x)
			cur.execute("select * from problem where problem_id=(?)",[x])
			cid=list(cur.fetchone())
			print (cid)
			con.commit()
		con.close()
		return render_template("preview.html",name=variable,title=cid[1],problem=cid[2], ca=cid[3], cw1=cid[4], cw2=cid[5], cw3=cid[6])


	tit=str(request.form['title'])
	print (submi+" ......... "+tit)
	if submi is not None and tit is not None and submi!="none" and tit!="none":
		print("you are in the check portion")
		with sql.connect("hack.db") as con:		
			cur=con.cursor()
			cur.execute("select problem_id from problem where title=(?) and course_id=(?)",[tit,c_id])
			pid=(cur.fetchone()[0])
			cur.execute("select correct_opt from problem where problem_id=(?)",[pid])
			right=(cur.fetchone()[0])
			cur.execute("select * from problem where problem_id=(?)",[pid])
			cid=(cur.fetchone())		
			con.commit()
		con.close()
		if (right==submi):
			print ("right answer")
		return jsonify({'right':right, 'submi':submi})
			

	stage=0
	typ=0
	with sql.connect("hack.db") as con:
		cur=con.cursor()
		cur.execute("select stage from progress")
		typ=cur.fetchone()[0]
	con.close()
	wrong = request.form['res']
	print ("wrong----------->",wrong)
	cid=[]
	print ("typesss ",type1,type2,type3);
	im=""
	if (typ==1):
		print ("type 1")
		with sql.connect("hack.db") as con:
			cur=con.cursor()
			cur.execute("SELECT img1 FROM course WHERE course_id= (?)",[c_id])
			im=cur.fetchone()[0]
			con.commit()
		con.close()
		
		if (len(type1)==1 and wrong=='1'):
			with sql.connect("hack.db") as con:
				cur=con.cursor()
				cur.execute("update progress set stage=2")
				cur.execute("SELECT problem_id FROM problem WHERE course_id= (?) and type=2",[c_id])
				x=cur.fetchall()
				for i in x:
					type2.append(i[0])
				random.shuffle(type2)
				con.commit()
			con.close()
			typ=2

		else:
			if wrong!='1':    #wrong answer
				with sql.connect("hack.db") as con:
					cur=con.cursor()
					type1.clear()
					cur.execute("SELECT problem_id FROM problem WHERE course_id= (?) and type=1",[c_id])
					x=cur.fetchall()
					for i in x:
						type1.append(i[0])
					random.shuffle(type1)
					with sql.connect("hack.db") as con:
						cur=con.cursor()
						cur.execute("select * from problem where problem_id=(?)",[type1[0]])
						cur.execute("update savedata set present=(?)",[type1[0]])
						cid=list(cur.fetchone())
						con.commit()
					con.close()
				con.close()
			else:
				print(type1)
				del type1[0]
				with sql.connect("hack.db") as con:
					cur=con.cursor()
					cur.execute("select * from problem where problem_id=(?)",[type1[0]])
					cid=list(cur.fetchone())
					cur.execute("update savedata set present=(?)",[type1[0]])
				
					con.commit()
				con.close()
	if (typ==2):
		print ("type 2")
		with sql.connect("hack.db") as con:
			cur=con.cursor()
			cur.execute("SELECT img2 FROM course WHERE course_id= (?)",[c_id])
			im=cur.fetchone()[0]
			con.commit()
		con.close()

		if (len(type2)==1 and wrong=='1'):
			with sql.connect("hack.db") as con:
				cur=con.cursor()
				cur.execute("update progress set stage=3")
				cur.execute("SELECT problem_id FROM problem WHERE course_id= (?) and type=3",[c_id])
				x=cur.fetchall()
				for i in x:
					type3.append(i[0])
				random.shuffle(type3)
				con.commit()
			con.close()
			typ=3
		
		else:
			if wrong!='1':    #wrong answer
				with sql.connect("hack.db") as con:
					cur=con.cursor()
					type2.clear()
					cur.execute("SELECT problem_id FROM problem WHERE course_id= (?) and type=2",[c_id])
					x=cur.fetchall()
					for i in x:
						type2.append(i[0])
					random.shuffle(type2)
					with sql.connect("hack.db") as con:
						cur=con.cursor()
						cur.execute("select * from problem where problem_id=(?)",[type2[0]])
						cid=list(cur.fetchone())
						cur.execute("update savedata set present=(?)",[type2[0]])
						con.commit()
					con.close()
				con.close()
			else:
				print(type2)
				del type2[0]
				with sql.connect("hack.db") as con:
					cur=con.cursor()
					cur.execute("select * from problem where problem_id=(?)",[type2[0]])
					cid=list(cur.fetchone())
					cur.execute("update savedata set present=(?)",[type2[0]])
					con.commit()
				con.close()
	if (typ==3):
		if (len(type3)==1 and wrong=='1'):
			###course end
			print ("course_ended")
		else:
			if wrong!='1':    #wrong answer
				with sql.connect("hack.db") as con:
					cur=con.cursor()
					type3.clear()
					cur.execute("SELECT problem_id FROM problem WHERE course_id= (?) and type=3",[c_id])
					x=cur.fetchall()
					for i in x:
						type3.append(i[0])
					random.shuffle(type3)
					with sql.connect("hack.db") as con:
						cur=con.cursor()
						cur.execute("select * from problem where problem_id=(?)",[type3[0]])
						cid=list(cur.fetchone())
						cur.execute("update savedata set present=(?)",[type3[0]])
						con.commit()
					con.close()
				con.close()
			else:
				print(type3)
				del type3[0]
				with sql.connect("hack.db") as con:
					cur=con.cursor()
					cur.execute("select * from problem where problem_id=(?)",[type1[0]])
					cid=list(cur.fetchone())
					cur.execute("update savedata set present=(?)",[type1[0]])
					con.commit()
				con.close()
			
	print ("CID--> ",cid)
	print (im)
	return render_template("preview.html",name=variable,title=cid[1],problem=cid[2], ca=cid[3], cw1=cid[4], cw2=cid[5], cw3=cid[6], img=im)

@app.route("/course/set-dependencies/<variable>", methods=["GET"])
def dependency(variable):
	c_name=variable.replace('-',' ')
	cid=1
	with sql.connect("hack.db") as con:
		curr=con.cursor()
		curr.execute("SELECT course_id FROM course WHERE course_name= (?)",[c_name])
		cid= (curr.fetchone()[0])
		con.commit()
	con.close()
	s=[]
	dep=[]
	with sql.connect("hack.db") as con:
		cur=con.cursor()
		cur.execute("SELECT title from problem where course_id=(?)",[cid])
		x=cur.fetchall()
		for i in x:
			s.append(i[0])
		cur.execute("SELECT  distinct x,y from dependencies where course_id=(?)",[cid])
		x=cur.fetchall()
		print (x)

		for i in x:
			l=[]
			l.append(i[0])
			l.append(i[1])
			dep.append(l)
	
	con.close()
	return render_template("dependencies.html", msg=s,x=dep,variable=variable)

@app.route("/course/set-dependencies/<variable>", methods=["POST","DELETE"])
def dependency_post(variable):
	if (flask.request.method=="DELETE"):
		print ("WE ARE IN DELETE METHOD")
		c_name=variable.replace('-',' ')
		option1=str(request.form['i1'])
		option2=str(request.form['i2'])
		print(option1,"---",option2)
		cid=1
		with sql.connect("hack.db") as con:
			curr=con.cursor()
			curr.execute("SELECT course_id FROM course WHERE course_name= (?)",[c_name])
			cid= (curr.fetchone()[0])
			curr.execute("DELETE FROM dependencies where x=(?) and y=(?)",(option1,option2))
			con.commit()
		con.close()
		s=[]
		dep=[]
		with sql.connect("hack.db") as con:
			cur=con.cursor()
			cur.execute("SELECT title from problem where course_id=(?)",[cid])
			x=cur.fetchall()
			for i in x:
				s.append(i[0])
			cur.execute("SELECT distinct x,y from dependencies where course_id=(?)",[cid])
			x=cur.fetchall()

			for i in x:
				l=[]
				l.append(i[0])
				l.append(i[1])
				dep.append(l)

		con.close()
		print (dep)
		return render_template("dependencies.html", msg=s,x=dep,variable=variable)
	else:
		c_name=variable.replace('-',' ')
		option1=request.form["val1"]
		option2=request.form["val2"]
		print (option1,"<-->",option2)
		print ("set dependencies post for-->" + c_name)
		cid=1
		with sql.connect("hack.db") as con:
			curr=con.cursor()
			curr.execute("SELECT course_id FROM course WHERE course_name= (?)",[c_name])
			cid=curr.fetchone()[0]
			if((option1!="None" and option2!="None") and (option1!="none" and option2!="none")) :
				print ("--------------------here-----------------------")
				curr.execute("INSERT INTO dependencies VALUES (?,?,?)",(option1,option2,cid))
			con.commit()
		con.close()
		s=[]
		dep=[]
		with sql.connect("hack.db") as con:
			cur=con.cursor()
			cur.execute("SELECT title from problem where course_id=(?)",[cid])
			x=cur.fetchall()
			print ("x--",x)
			for i in x:
				s.append(i[0])
			cur.execute("SELECT distinct x,y from dependencies where course_id=(?)",[cid])
			x=cur.fetchall()
			print ("x---",x)
			for i in x:
				l=[]
				l.append(i[0])
				l.append(i[1])
				dep.append(l)
		con.close()
		return render_template("dependencies.html", msg=s,x=dep,variable=variable)

