// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
import "@chainlink/contracts/src/v0.8/ChainlinkClient.sol";

contract Oracle is ChainlinkClient {
    mapping(uint => uint) public collateralizations;
    
    address private oracle;
    bytes32 private jobId;
    uint256 private fee;

    // constructor() {
    //     setPublicChainlinkToken();
    //     oracle = 0xc57B33452b4F7BB189bB5AfaE9cc4aBa1f7a4FD8;
    //     jobId = "d5270d1c311941d0b08bead21fea7747";
    //     fee = 0.1 * 10 ** 18; // 0.1 LINK
    // }

    function requestCollateralization(uint userId) public {
        Chainlink.Request memory request = buildChainlinkRequest(jobId, address(this), this.fulfill.selector);
        request.add("get", "https://myapi.com/users/$(userId)/collateralization");
        request.add("path", "collateralization");
        request.add("queryParams", "userId");
        request.addInt("userId", int(userId));
        sendChainlinkRequestTo(oracle, request, fee);
    }

    function fulfill(bytes32 requestId, uint256 collateralization) public recordChainlinkFulfillment(requestId) {
        // Store the returned collateralization for the corresponding user
        uint userId = uint(requestId);
        collateralizations[userId] = collateralization;
    }

    function setCollateralization(uint user_id, uint collateralization) external {
        collateralizations[user_id] = collateralization;
    }

    function getCollateralization(uint user_id) external view returns (uint) {
        return collateralizations[user_id];
    }
}
