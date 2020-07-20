pragma solidity ^0.4.26;

contract StudentManagement{
    
    address admin;
    uint256 studentCount;
    uint256 subjectCount;
    
     constructor() public{
        admin =msg.sender;
    }
    
    
    modifier AdminOnly {
        require(msg.sender==admin);
        _;
    }
    
     struct SubjectDetails{
        uint ComputerScience;
        uint Maths;
        uint DigitaElectronics;
        uint DataScience;
    }
    
    struct Student{
        string name;
        uint student_id;
        string batch;
        string stream;
        uint time;
        address addedBy;
        uint attendanceCount;
        SubjectDetails subjects;
    }
    
    mapping( uint256 => Student ) public studentList;
    mapping( uint256 => SubjectDetails ) public marksList;

   function authorizeAdmin(address _newAdmin) public AdminOnly{
       admin=_newAdmin;
   }
    
    function newStudent(string memory _name, uint _id, string memory _batch, string memory _stream) public AdminOnly{
        require(_id>0);
        require(bytes(_name).length>0);
        studentCount++;
        studentList[studentCount]=Student(_name,_id,_batch,_stream,now,msg.sender,0,SubjectDetails(0,0,0,0));
        
    }
    
    function addAttendance(uint _index) public AdminOnly{
        studentList[_index].attendanceCount+=1;
    }

    function addSubjectMarks(uint _index,uint _compMarks, uint _mathMarks, uint _deMarks, uint _dsMarks) public AdminOnly{
        Student memory _stu = studentList[_index];
        _stu.subjects.ComputerScience=_compMarks;
        _stu.subjects.Maths=_mathMarks;
        _stu.subjects.DigitaElectronics=_deMarks;
        _stu.subjects.DataScience=_dsMarks;
        _stu.addedBy = msg.sender;
        studentList[_index]=_stu;
        
        subjectCount++;
        marksList[subjectCount] = SubjectDetails(_compMarks,_mathMarks,_deMarks,_dsMarks);
    }
}









