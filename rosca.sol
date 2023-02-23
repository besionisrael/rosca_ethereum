// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ROSCA {
    mapping(address => bool) public members;
    mapping(address => address[]) public graph;
    address[] public memberList;
    uint[][] public edges;
    event Log(string message);

    function form_ROSCA(uint[][] memory edgeList) external {
        
        edges = edgeList;
        uint n = edgeList.length;
        
        // Add the users to the ROSCA
        for (uint i = 0; i < n; i++) {
            address user = address(uint160(edges[i][0]));
            if (!members[user]){
                members[user] = true;
                memberList.push(user);

            }
        }
    }

    function getMemberList() external view returns (address[] memory) {
        return memberList;
    }

    function getSubgroups() external returns (address[][] memory) {

        // First Convert the list of edges to a graph
        for (uint i = 0; i < edges.length; i++) {
            address user1 = address(uint160(edges[i][0]));
            address user2 = address(uint160(edges[i][1]));

            if (!members[user1]) {
                members[user1] = true;
                memberList.push(user1);
                graph[user1] = new address[](0);
            }

            if (!members[user2]) {
                members[user2] = true;
                memberList.push(user2);
                graph[user2] = new address[](0);
            }

            graph[user1].push(user2);
            graph[user2].push(user1);
        }
        

        uint n = memberList.length;
        bool[] memory visited = new bool[](n);
        address[][] memory subgroups = new address[][](0);

        for (uint i = 0; i < n; i++) {
            if (!visited[i]) {
                address[] memory subgroup = new address[](0);
                traverse(memberList[i], visited, subgroup);
                subgroups = push(subgroups, subgroup);
            }
        }

        return subgroups;
    }

    function traverse(address user, bool[] memory visited, address[] memory subgroup) internal view {
        visited[getMemberIndex(user)] = true;
        subgroup = pushAddr(subgroup, user);

        for (uint i = 0; i < graph[user].length; i++) {
            address adjacentUser = graph[user][i];
            uint adjacentUserIndex = getMemberIndex(adjacentUser);

            if (!visited[adjacentUserIndex]) {
                traverse(adjacentUser, visited, subgroup);
            }
        }
    }

    function push(address[][] memory arr, address[] memory val) internal pure returns (address[][] memory) {
        address[][] memory newarr = new address[][](arr.length + 1);
        for (uint i = 0; i < arr.length; i++) {
            newarr[i] = arr[i];
        }
        newarr[arr.length] = val;
        return newarr;
    }

    function pushAddr(address[] memory array, address item) internal pure returns (address[] memory) {
        address[] memory newArray = new address[](array.length + 1);

        for (uint i = 0; i < array.length; i++) {
            newArray[i] = array[i];
        }
        newArray[array.length] = item;
        return newArray;
    }

    function getMemberIndex(address member) internal view returns (uint) {
        for (uint i = 0; i < memberList.length; i++) {
            if (memberList[i] == member) {
                return i;
            }
        }

        revert("Member not found");
    }
    
}
